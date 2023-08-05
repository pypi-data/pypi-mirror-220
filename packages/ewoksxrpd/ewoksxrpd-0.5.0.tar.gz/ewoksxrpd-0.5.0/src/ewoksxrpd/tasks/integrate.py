import logging
from numbers import Number
from contextlib import contextmanager, ExitStack
from typing import Union, Tuple, List, Dict, Optional, Any

import numpy
import h5py
from ewoksdata.data.hdf5.dataset_writer import DatasetWriter

from .worker import persistent_worker
from .worker import set_maximum_persistent_workers
from .utils import data_utils, xrpd_utils, pyfai_utils, integrate_utils
from .data_access import TaskWithDataAccess


__all__ = ["Integrate1D", "IntegrateBlissScan", "IntegrateBlissScanWithoutSaving"]


logger = logging.getLogger(__name__)


class _BaseIntegrate(
    TaskWithDataAccess,
    input_names=["detector", "geometry", "energy"],
    optional_input_names=[
        "detector_config",
        "mask",
        "flatfield",
        "darkcurrent",
        "integration_options",
        "fixed_integration_options",
        "maximum_persistent_workers",
        "references",
        "monitors",
    ],
    register=False,
):
    @contextmanager
    def _worker(self):
        nworkers = self.get_input_value("maximum_persistent_workers", None)
        if nworkers is not None:
            set_maximum_persistent_workers(nworkers)
        options = self._get_pyfai_options()
        with persistent_worker(options) as worker:
            yield worker, options

    def _get_pyfai_options(self) -> dict:
        geometry = data_utils.data_from_storage(self.inputs.geometry)
        xrpd_utils.validate_geometry(geometry)
        integration_options = data_utils.data_from_storage(
            self.inputs.integration_options, remove_numpy=True
        )
        fixed_integration_options = data_utils.data_from_storage(
            self.get_input_value("fixed_integration_options", None), remove_numpy=True
        )
        config = dict()
        if integration_options:
            config.update(integration_options)
        if fixed_integration_options:
            config.update(fixed_integration_options)
        if geometry:
            config.update(geometry)

        config.setdefault("unit", "2th_deg")
        config["detector"] = data_utils.data_from_storage(self.inputs.detector)
        config["detector_config"] = data_utils.data_from_storage(
            self.get_input_value("detector_config", None)
        )
        config["wavelength"] = xrpd_utils.energy_wavelength(self.inputs.energy)
        if not self.missing_inputs.mask and self.inputs.mask is not None:
            config["mask"] = self.get_image(
                data_utils.data_from_storage(self.inputs.mask)
            )
        if not self.missing_inputs.flatfield and self.inputs.flatfield is not None:
            config["flatfield"] = self.get_image(
                data_utils.data_from_storage(self.inputs.flatfield)
            )
        if not self.missing_inputs.darkcurrent and self.inputs.darkcurrent is not None:
            config["darkcurrent"] = self.get_image(
                data_utils.data_from_storage(self.inputs.darkcurrent)
            )
        return config

    def _pyfai_normalization_factor(
        self,
        monitors: List[Union[numpy.ndarray, Number, str, list, None]],
        references: List[Union[numpy.ndarray, Number, str, list, None]],
        ptdata: Optional[Dict[str, numpy.ndarray]] = None,
    ) -> Tuple[float, float]:
        r"""Returns the pyfai normalization factor based on a monitor and a references.

        The pyfai normalization factor is defined as

        .. code::

            Inorm = I / (normalization_factor1 * normalization_factor2 * ...)

        Monitor normalization is done like this

        .. code::

            Inorm = I * reference1 / monitor1 * reference2 / monitor2 * ...

        which means that the normalization factor is

        .. code::

            normalization_factor = monitor1 / reference1 * monitor2 / reference2 * ...

        Both monitors and references can be defined by:

         * scalar value
         * array or list of numbers
         * counter name
         * data URL
        """
        numerator = 1.0
        for value in monitors:
            if not data_utils.is_data(value):
                value = 1
            elif _is_counter_name(value):
                if ptdata is None:
                    raise ValueError("monitor value cannot be a counter name")
                value = ptdata[value]
            else:
                value = self.get_data(value)
            numerator *= value

        if not numpy.isscalar(numerator):
            raise ValueError("monitor values need to be scalars")

        denominator = 1.0
        for value in references:
            if not data_utils.is_data(value):
                value = 1
            elif _is_counter_name(value):
                if ptdata is None:
                    raise ValueError("reference value cannot be a counter name")
                value = ptdata[value]
            else:
                value = self.get_data(value)
            denominator *= value

        if not numpy.isscalar(denominator):
            raise ValueError("reference values need to be scalars")

        return numerator, denominator


class Integrate1D(
    _BaseIntegrate,
    input_names=["image"],
    optional_input_names=["monitor", "reference"],
    output_names=["x", "y", "yerror", "xunits", "info"],
):
    """1D integration of a single diffraction pattern."""

    def run(self):
        raw_data = self.get_image(self.inputs.image)

        monitors = self.get_input_value("monitors", list())
        references = self.get_input_value("references", list())
        if len(monitors) != len(references):
            raise ValueError(
                "length of normalization monitors and references is not the same"
            )
        if not self.missing_inputs.monitor or not self.missing_inputs.reference:
            monitors.append(self.get_input_value("monitor", None))
            references.append(self.get_input_value("reference", None))

        monitor_value, reference_value = self._pyfai_normalization_factor(
            monitors, references
        )
        normalization_factor = monitor_value / reference_value

        with self._worker() as (worker, config):
            result = worker.process(raw_data, normalization_factor=normalization_factor)

            self.outputs.x = result.radial
            self.outputs.y = result.intensity
            yerror = integrate_utils.get_yerror(result)
            self.outputs.yerror = numpy.abs(yerror)
            self.outputs.xunits = result.unit.name

            info = pyfai_utils.compile_integration_info(
                config,
                monitor_value=monitor_value,
                reference_value=reference_value,
            )
            self.outputs.info = info


class IntegrateBlissScan(
    _BaseIntegrate,
    input_names=["filename", "scan", "detector_name", "output_filename"],
    optional_input_names=[
        "counter_names",
        "monitor_name",
        "reference",
        "subscan",
        "retry_timeout",
        "retry_period",
        "demo",
        "scan_memory_url",
        "external_output_filename",
        "nxprocess_name",
        "nxmeasurement_name",
        "nxprocess_as_default",
        "flush_period",
    ],
    output_names=["nxdata_url"],
):
    """1D or 2D integration of a single detector in a single Bliss scan with saving."""

    def run(self):
        if self.inputs.counter_names:
            counter_names = set(self.inputs.counter_names)
        else:
            counter_names = set()

        detector_name = self.inputs.detector_name

        monitors = self.get_input_value("monitors", list())
        references = self.get_input_value("references", list())
        if len(monitors) != len(references):
            raise ValueError(
                "length of normalization monitors and references is not the same"
            )
        if not self.missing_inputs.monitor_name or not self.missing_inputs.reference:
            monitors.append(self.get_input_value("monitor_name", None))
            references.append(self.get_input_value("reference", None))
        for name in references:
            if _is_counter_name(name):
                counter_names.add(name)
        for name in monitors:
            if _is_counter_name(name):
                counter_names.add(name)
        counter_names = list(counter_names)

        scan = self.inputs.scan
        subscan = self.get_input_value("subscan", 1)
        output_filename = self.inputs.output_filename
        output_url = f"silx://{output_filename}?path=/{scan}.{subscan}"
        external_output_filename = self.get_input_value(
            "external_output_filename", output_filename
        )
        external_output_url = (
            f"silx://{external_output_filename}?path=/{scan}.{subscan}"
        )
        input_url = f"silx://{self.inputs.filename}?path=/{scan}.{subscan}"
        flush_period = self.get_input_value("flush_period", None)

        with ExitStack() as stack:
            worker = None
            data_parent = None
            master_parent = None
            nxprocess = None
            measurement = None

            intensity_writer = None
            error_writer = None
            ctr_writers = dict()

            if self.inputs.scan_memory_url:
                logger.info("PyFAI integrate data from %r", self.inputs.scan_memory_url)
                data_iterator = self.iter_bliss_data_from_memory(
                    self.inputs.scan_memory_url,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                )
            else:
                logger.info(
                    "PyFAI integrate data from '%s::%d.%d'",
                    self.inputs.filename,
                    self.inputs.scan,
                    subscan,
                )
                data_iterator = self.iter_bliss_data(
                    self.inputs.filename,
                    self.inputs.scan,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                    subscan=subscan,
                )

            for ptdata in data_iterator:
                if worker is None:
                    # Start the worker + open the output file only after
                    # the first image is read
                    worker, config = stack.enter_context(self._worker())
                    info = pyfai_utils.compile_integration_info(
                        config,
                        monitors=monitors,
                        references=references,
                    )

                    data_parent = stack.enter_context(
                        self.open_h5item(external_output_url, mode="a", create=True)
                    )
                    assert isinstance(data_parent, h5py.Group)

                    with self.open_h5item(
                        output_url, mode="a", create=True
                    ) as master_parent:
                        assert isinstance(master_parent, h5py.Group)
                        nxprocess = pyfai_utils.create_nxprocess(
                            master_parent, data_parent, self._nxprocess_name, info
                        )
                        if counter_names:
                            measurement = data_parent.require_group("measurement")
                            measurement.attrs["NX_class"] = "NXcollection"
                            if data_parent.file.filename != master_parent.file.filename:
                                pyfai_utils.create_hdf5_link(
                                    measurement, master_parent, "measurement"
                                )

                monitor_value, reference_value = self._pyfai_normalization_factor(
                    monitors, references, ptdata
                )
                normalization_factor = monitor_value / reference_value

                image = ptdata[detector_name]
                if self.inputs.demo:
                    image = image[:-1, :-1]
                result = worker.process(
                    image, normalization_factor=normalization_factor
                )
                if intensity_writer is None:
                    nxdata = pyfai_utils.create_nxdata(
                        nxprocess,
                        result.intensity.ndim + 1,  # +1 for the scan dimension
                        result.radial,
                        result.unit,
                        result.azimuthal if result.intensity.ndim == 2 else None,
                    )
                    intensity_writer = stack.enter_context(
                        DatasetWriter(nxdata, "intensity", flush_period=flush_period)
                    )
                    if result.sigma is not None:
                        error_writer = stack.enter_context(
                            DatasetWriter(
                                nxdata, "intensity_errors", flush_period=flush_period
                            )
                        )
                    for name in counter_names:
                        ctr_writers[name] = stack.enter_context(
                            DatasetWriter(measurement, name, flush_period=flush_period)
                        )

                flush = intensity_writer.add_point(result.intensity)
                if result.sigma is not None:
                    flush |= error_writer.add_point(result.sigma)
                for name in counter_names:
                    flush |= ctr_writers[name].add_point(ptdata[name])
                if flush:
                    data_parent.file.flush()

            if intensity_writer is None:
                raise RuntimeError("No scan data")
            intensity_writer.flush_buffer()
            if error_writer is not None:
                error_writer.flush_buffer()

            nxdata["points"] = numpy.arange(intensity_writer.dataset.shape[0])
            axes = nxdata.attrs["axes"]
            axes[0] = "points"
            nxdata.attrs["axes"] = axes

            with self.open_h5item(output_url, mode="a", create=True) as master_parent:
                self.link_bliss_scan(master_parent, input_url)
                mark_as_default = self.get_input_value("nxprocess_as_default", True)
                measurement = master_parent.require_group("measurement")
                measurement.attrs["NX_class"] = "NXcollection"
                pyfai_utils.create_nxprocess_links(
                    nxprocess,
                    measurement,
                    self._nxmeasurement_name,
                    mark_as_default=mark_as_default,
                )

            self.outputs.nxdata_url = f"{nxdata.file.filename}::{nxdata.name}"

    @property
    def _nxprocess_name(self):
        if self.inputs.nxprocess_name:
            return self.inputs.nxprocess_name
        default = "integrate"
        if self.inputs.detector_name:
            return f"{self.inputs.detector_name}_{default}"
        return default

    @property
    def _nxmeasurement_name(self):
        if self.inputs.nxmeasurement_name:
            return self.inputs.nxmeasurement_name
        default = "integrated"
        if self.inputs.detector_name:
            return f"{self.inputs.detector_name}_{default}"
        return default


class IntegrateBlissScanWithoutSaving(
    _BaseIntegrate,
    input_names=["filename", "scan", "detector_name"],
    optional_input_names=[
        "counter_names",
        "monitor_name",
        "reference",
        "subscan",
        "retry_timeout",
        "retry_period",
        "demo",
        "scan_memory_url",
    ],
    output_names=[
        "radial",
        "azimuthal",
        "intensity",
        "intensity_error",
        "radial_units",
        "info",
    ],
):
    """1D or 2D integration of a single detector in a single Bliss scan without saving."""

    def run(self):
        with self._worker() as (worker, config):
            if self.inputs.counter_names:
                counter_names = set(self.inputs.counter_names)
            else:
                counter_names = set()
            detector_name = self.inputs.detector_name

            monitors = self.get_input_value("monitors", list())
            references = self.get_input_value("references", list())
            if len(monitors) != len(references):
                raise ValueError(
                    "length of normalization monitors and references is not the same"
                )
            if (
                not self.missing_inputs.monitor_name
                or not self.missing_inputs.reference
            ):
                monitors.append(self.get_input_value("monitor_name", None))
                references.append(self.get_input_value("reference", None))
            for name in references:
                if _is_counter_name(name):
                    counter_names.add(name)
            for name in monitors:
                if _is_counter_name(name):
                    counter_names.add(name)
            counter_names = list(counter_names)

            subscan = self.get_input_value("subscan", None)

            intensities = []
            sigmas = []
            radial = None
            unit = None
            azimuthal = None

            if self.inputs.scan_memory_url:
                logger.info("PyFAI integrate data from %r", self.inputs.scan_memory_url)
                data_iterator = self.iter_bliss_data_from_memory(
                    self.inputs.scan_memory_url,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                )
            else:
                logger.info(
                    "PyFAI integrate data from '%s::%d.%s'",
                    self.inputs.filename,
                    self.inputs.scan,
                    subscan,
                )
                data_iterator = self.iter_bliss_data(
                    self.inputs.filename,
                    self.inputs.scan,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                    subscan=subscan,
                )

            normalization_factor = 0
            for ptdata in data_iterator:
                monitor_value, reference_value = self._pyfai_normalization_factor(
                    monitors, references, ptdata
                )
                normalization_factor = monitor_value / reference_value
                image = ptdata[detector_name]
                if self.inputs.demo:
                    image = image[:-1, :-1]
                result = worker.process(
                    image, normalization_factor=normalization_factor
                )

                intensities.append(result.intensity)
                sigmas.append(integrate_utils.get_yerror(result))
                if radial is None:
                    radial = result.radial
                if unit is None:
                    unit = result.unit.name
                if worker.do_2D() and azimuthal is None:
                    azimuthal = result.azimuthal

            info = pyfai_utils.compile_integration_info(
                config, monitors=monitors, references=references
            )

            self.outputs.radial = radial
            self.outputs.azimuthal = azimuthal
            self.outputs.intensity = numpy.array(intensities)
            self.outputs.intensity_error = numpy.array(sigmas)
            self.outputs.radial_units = unit
            self.outputs.info = info


def _is_counter_name(value: Any) -> bool:
    return isinstance(value, str) and "://" not in value
