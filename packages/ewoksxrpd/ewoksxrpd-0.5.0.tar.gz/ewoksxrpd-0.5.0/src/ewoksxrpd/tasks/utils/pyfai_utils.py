import os
import re
import json
from typing import Union, Dict, Optional, Any, Iterator, Tuple, List
from collections.abc import Mapping, Sequence

import numpy
import h5py
from pyFAI import version as pyfai_version
from ewoks import __version__ as ewoks_version
from pyFAI.io.ponifile import PoniFile
from pyFAI.units import Unit
from silx.io.dictdump import dicttonx
from ewokscore.task import TaskInputError
from ewoksdata.data import nexus
from ewokscore.missing_data import is_missing_data

from .xrpd_utils import energy_wavelength
from .data_utils import data_from_storage

_REPLACE_PATTERNS = {
    "/gpfs/[^/]+/": "/",
    "/mnt/multipath-shares/": "/",
    "/lbsram/": "/",
}


def parse_units(radial_units: Any) -> Tuple[str, str]:
    if isinstance(radial_units, Unit):
        radial_units = radial_units.name
    if isinstance(radial_units, numpy.ndarray):
        radial_units = radial_units.item()
    if not isinstance(radial_units, str):
        raise TypeError(type(radial_units))
    unit_tuple = tuple(radial_units.split("_"))
    if len(unit_tuple) != 2:
        raise ValueError(f"Expected unit to be of the form X_Y. Got {radial_units}")
    return unit_tuple


def read_config(
    filename: Optional[str], replace_patterns: Optional[Dict[str, str]] = None
) -> dict:
    if not filename:
        return dict()
    if filename.endswith(".json"):
        parameters = _read_json(filename)
    else:
        parameters = _read_poni(filename)
    return normalize_parameters(parameters, replace_patterns=replace_patterns)


def _read_json(filename: str) -> dict:
    with open(filename, "r") as fp:
        return json.load(fp)


def _read_poni(filename: str) -> dict:
    return PoniFile(filename).as_dict()


def normalize_parameters(
    parameters: Union[str, int, float, Mapping, Sequence],
    replace_patterns: Optional[Dict[str, str]] = None,
) -> Union[str, int, float, Mapping, Sequence]:
    if replace_patterns is None:
        replace_patterns = _REPLACE_PATTERNS
    if isinstance(parameters, str):
        for pattern, repl in replace_patterns.items():
            parameters = re.sub(pattern, repl, parameters)
        return parameters
    if isinstance(parameters, Mapping):
        return {
            k: normalize_parameters(v, replace_patterns=replace_patterns)
            for k, v in parameters.items()
        }
    if isinstance(parameters, Sequence):
        return [
            normalize_parameters(v, replace_patterns=replace_patterns)
            for v in parameters
        ]
    return parameters


def extract_mask(integration_options: dict) -> Optional[numpy.ndarray]:
    """Integration options related to the mask:

    * mask_file: URL or None
    * do_mask: use mask_file or not
    * mask: URL, array or None (overwrites mask_file and do_mask when not None)
    """
    # Typically from a JSON configuration file
    mask_file = integration_options.get("mask_file", None)
    do_mask = integration_options.get("do_mask", None)
    if not do_mask:
        mask_file = None

    # Typically in memory from a previous calculation
    mask = integration_options.pop("mask", None)
    if isinstance(mask, str):
        mask_file = mask
        mask = None
        do_mask = True

    # Let pyFAI handle URLs (if any) and return in-memory (if any)
    integration_options["mask_file"] = mask_file
    integration_options["do_mask"] = do_mask
    return mask


def extract_flatfield(integration_options: dict) -> Optional[numpy.ndarray]:
    """Integration options related to the flatfield:

    * flat_field: URL(s) (list of strings or comma separate string) or None
    * do_flat: use flat_field or not
    * flatfield: URL(s) (list of strings or comma separate string), array or None (overwrites flat_field and do_flat when not None)
    """
    # Typically from a JSON configuration file
    flat_field = integration_options.get("flat_field", None)
    do_flat = integration_options.get("do_flat", None)
    if not do_flat:
        flat_field = None

    # Typically in memory from a previous calculation
    flatfield = integration_options.pop("flatfield", None)
    if isinstance(flatfield, str):
        flatfield = [s.strip() for s in flatfield.split(",")]
    if isinstance(flatfield, Sequence) and isinstance(flatfield[0], str):
        flat_field = flatfield
        flatfield = None
        do_flat = True

    # Let pyFAI handle URLs (if any) and return in-memory (if any)
    integration_options["flat_field"] = flat_field
    integration_options["do_flat"] = do_flat
    return flatfield


def extract_darkcurrent(integration_options: dict) -> Optional[numpy.ndarray]:
    """Integration options related to the dark-current:

    * dark_current: URL(s) (list of strings or comma separate string) or None
    * do_dark: use flat_field or not
    * darkcurrent: URL(s) (list of strings or comma separate string), array or None (overwrites dark_current and do_dark when not None)
    """
    # Typically from a JSON configuration file
    dark_current = integration_options.get("dark_current", None)
    do_dark = integration_options.get("do_dark", None)
    if not do_dark:
        dark_current = None

    # Typically in memory from a previous calculation
    darkcurrent = integration_options.pop("darkcurrent", None)
    if isinstance(darkcurrent, str):
        darkcurrent = [s.strip() for s in darkcurrent.split(",")]
    if isinstance(darkcurrent, Sequence) and isinstance(darkcurrent[0], str):
        dark_current = darkcurrent
        darkcurrent = None
        do_dark = True

    # Let pyFAI handle URLs (if any) and return in-memory (if any)
    integration_options["dark_current"] = dark_current
    integration_options["do_dark"] = do_dark
    return darkcurrent


def compile_integration_info(parameters: Mapping, **extra) -> Dict[str, Any]:
    """Compile information on a pyFAI integration process. Add and rename keys when appropriate."""
    integration_info = dict(parameters)

    mask = extract_mask(integration_info)
    flatfield = extract_flatfield(integration_info)
    darkcurrent = extract_darkcurrent(integration_info)

    # Do not save the in-memory make, flat field and dark current
    if mask is not None:
        integration_info["mask_file"] = "[...]"
    if flatfield is not None:
        integration_info["flat_field"] = "[...]"
    if darkcurrent is not None:
        integration_info["dark_current"] = "[...]"

    for k, v in extra.items():
        if v is not None:
            integration_info[k] = v
    wavelength = integration_info.get("wavelength")
    if wavelength is not None:
        integration_info["energy"] = energy_wavelength(wavelength)
    return integration_info


def integration_info_for_text(integration_info: Mapping, **extra) -> List[str]:
    """Convert to a flat list of strings with the format `{key} = {value}`.
    Add keys and units when appropriate.
    """
    flatdict = {"pyfai_version": pyfai_version, "ewoks_version": ewoks_version}
    flatdict.update(integration_info)
    _add_extra(flatdict, extra)
    flatdict = dict(_flatten_dict(flatdict))

    energy = flatdict.pop("energy", None)
    if energy:
        flatdict["energy"] = f"{energy:.18e} keV"

    wavelength = flatdict.pop("wavelength", None)
    if wavelength is not None:
        flatdict["wavelength"] = f"{wavelength:.18e} m"

    geometry_dist = flatdict.pop("geometry.dist", None)
    if geometry_dist is not None:
        flatdict["distance"] = f"{geometry_dist:.18e} m"

    geometry_poni1 = flatdict.pop("geometry.poni1", None)
    if geometry_poni1 is not None:
        flatdict["center dim0"] = f"{geometry_poni1:.18e} m"

    geometry_poni2 = flatdict.pop("geometry.poni2", None)
    if geometry_poni2 is not None:
        flatdict["center dim1"] = f"{geometry_poni2:.18e} m"

    geometry_rot1 = flatdict.pop("geometry.rot1", None)
    if geometry_rot1 is not None:
        flatdict["rot1"] = f"{geometry_rot1:.18e} rad"

    geometry_rot2 = flatdict.pop("geometry.rot2", None)
    if geometry_rot2 is not None:
        flatdict["rot2"] = f"{geometry_rot2:.18e} rad"

    geometry_rot3 = flatdict.pop("geometry.rot3", None)
    if geometry_rot3 is not None:
        flatdict["rot3"] = f"{geometry_rot3:.18e} rad"

    return [f"{k} = {v}" for k, v in flatdict.items()]


def integration_info_for_nexus(
    integration_info, as_nxnote: bool = True, **extra
) -> Dict[str, Any]:
    """Convert to a Nexus dictionary. Add keys and units when appropriate."""
    configuration = {"ewoks_version": ewoks_version}
    configuration.update(integration_info)
    nxtree_dict = {
        "@NX_class": "NXprocess",
        "program": "pyFAI",
        "version": pyfai_version,
    }
    if as_nxnote:
        nxtree_dict["configuration"] = {
            "@NX_class": "NXnote",
            "type": "application/json",
            "data": json.dumps(configuration, cls=PyFaiEncoder),
        }
    else:
        configuration["@NX_class"] = "NXcollection"
        nxtree_dict["configuration"] = configuration
        if "energy" in configuration:
            configuration["energy@units"] = "keV"
        if "wavelength" in configuration:
            configuration["wavelength@units"] = "m"
        geometry = configuration.get("geometry", dict())
        if "dist" in geometry:
            geometry["dist@units"] = "m"
        if "poni1" in geometry:
            geometry["poni1@units"] = "m"
        if "poni2" in geometry:
            geometry["poni1@units"] = "m"
        if "rot1" in geometry:
            geometry["rot1@units"] = "rad"
        if "rot2" in geometry:
            geometry["rot2@units"] = "rad"
        if "rot3" in geometry:
            geometry["rot3@units"] = "rad"
    _add_extra(nxtree_dict, extra)
    return nxtree_dict


class PyFaiEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (numpy.generic, numpy.ndarray)):
            return obj.tolist()
        return super().default(obj)


def _flatten_dict(
    adict: Mapping, _prefix: Optional[str] = None
) -> Iterator[Tuple[str, Any]]:
    if _prefix is None:
        _prefix = ""
    for k, v in adict.items():
        k = _prefix + k
        if isinstance(v, Mapping):
            yield from _flatten_dict(v, _prefix=f"{k}.")
        else:
            yield k, v


def _add_extra(adict: Mapping, extra: Mapping):
    for k, v in extra.items():
        if v is not None:
            adict[k] = v


def create_nxprocess(
    master_parent: h5py.Group, data_parent: h5py.Group, nxprocess_name: str, info
) -> h5py.Group:
    nxtree_dict = integration_info_for_nexus(info, integrated={"@NX_class": "NXdata"})
    nxprocess_path = f"{data_parent.name}/{nxprocess_name}"
    dicttonx(nxtree_dict, data_parent.file, h5path=nxprocess_path, update_mode="modify")
    nxprocess = data_parent[nxprocess_name]
    if data_parent.file.filename != master_parent.file.filename:
        create_hdf5_link(nxprocess, master_parent, nxprocess_name)
    return nxprocess


def create_nxdata(
    nxprocess: h5py.Group, intensity_dim: int, radial, radial_units, azimuthal
) -> h5py.Group:
    # Axes names and units
    radial_units = data_from_storage(radial_units, remove_numpy=True)
    try:
        radial_name, radial_units = parse_units(radial_units)
    except ValueError as e:
        raise TaskInputError(e)
    has_azimuth = not is_missing_data(azimuthal) and azimuthal is not None
    azimuthal_name = "azimuth"
    azimuthal_units = "deg"

    # Axes interpretation
    nxdata = nxprocess["integrated"]
    nxprocess.attrs["default"] = "integrated"
    if has_azimuth and intensity_dim == 2:
        nxdata.attrs["axes"] = [azimuthal_name, radial_name]
        nxdata.attrs["interpretation"] = "image"
    elif has_azimuth and intensity_dim == 3:
        nxdata.attrs["axes"] = [".", azimuthal_name, radial_name]
        nxdata.attrs["interpretation"] = "image"
    elif not has_azimuth and intensity_dim == 2:
        nxdata.attrs["axes"] = [".", radial_name]
        nxdata.attrs["interpretation"] = "spectrum"
    elif not has_azimuth and intensity_dim == 1:
        nxdata.attrs["axes"] = [radial_name]
        nxdata.attrs["interpretation"] = "spectrum"
    else:
        raise ValueError("Unrecognized data")

    # Prepare for signal
    nxdata.attrs["signal"] = "intensity"

    # Save axes
    dset = nxdata.create_dataset(radial_name, data=radial)
    dset.attrs["units"] = radial_units
    if has_azimuth:
        dset = nxdata.create_dataset(azimuthal_name, data=azimuthal)
        dset.attrs["units"] = azimuthal_units

    return nxdata


def create_nxprocess_links(
    nxprocess: h5py.Group,
    target: h5py.Group,
    link_name: str,
    mark_as_default: bool = True,
) -> None:
    nxdata = nxprocess["integrated"]
    try:
        intensity = nxdata["intensity"]
    except KeyError:
        return
    create_hdf5_link(intensity, target, link_name)
    if mark_as_default:
        nexus.select_default_plot(intensity)
        if intensity.file.filename != nxprocess.file.filename:
            target.attrs["default"] = link_name
            nexus.select_default_plot(target)


def create_hdf5_link(
    source: Union[h5py.Dataset, h5py.Group], target: h5py.Group, link_name: str
) -> None:
    if link_name in target:
        return
    source_filename = source.file.filename
    target_filename = target.file.filename
    if source_filename == target_filename:
        target[link_name] = h5py.SoftLink(source.name)
    else:
        source_filename = os.path.relpath(
            source_filename, os.path.dirname(target_filename)
        )
        target[link_name] = h5py.ExternalLink(source_filename, source.name)
