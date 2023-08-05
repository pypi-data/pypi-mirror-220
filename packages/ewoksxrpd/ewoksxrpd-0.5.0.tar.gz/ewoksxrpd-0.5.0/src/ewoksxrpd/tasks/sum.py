from typing import Optional
from ewokscore import Task
import h5py
import numpy


def generate_range(start: int, end_arg: Optional[int], nitems: int) -> range:
    end = nitems if end_arg is None else end_arg + 1

    if (end - start) > nitems:
        raise ValueError(
            f"Asked range ({start},{end}) is bigger than number of items ({nitems})"
        )

    return range(start, end)


def save_sum(
    nxdata: h5py.Group, name: str, data: numpy.ndarray, nb_images: int, monitor: int
):
    dset = nxdata.create_dataset(name, data=data)
    dset.attrs["monitor"] = monitor
    dset.attrs["nb_images"] = nb_images

    if "signal" not in nxdata:
        nxdata["signal"] = name

    return dset


class SumImages(
    Task,
    input_names=["filename", "detector_name", "output_file"],
    optional_input_names=[
        "start_scan",
        "end_scan",
        "exclude_scans",
        "start_image",
        "end_image",
        "step",
        "monitor_name",
        "output_entry",
        "output_process",
    ],
    output_names=["output_uris"],
):
    """Sum images of a single camera from a Bliss scan file"""

    def run(self):
        filename: str = self.inputs.filename
        detector_name: str = self.inputs.detector_name
        output_file: str = self.inputs.output_file
        start_scan: int = self.get_input_value("start_scan", 1)
        end_scan: Optional[int] = self.get_input_value("end_scan", None)
        start_image: int = self.get_input_value("start_image", 0)
        end_image: Optional[int] = self.get_input_value("end_image", None)
        step: Optional[int] = self.get_input_value("step", None)
        monitor_name: Optional[str] = self.get_input_value("monitor_name", None)
        output_entry: str = self.get_input_value("output_entry", "processing")
        output_process: str = self.get_input_value("output_process", "sum")

        with h5py.File(filename, "r") as h5file:
            nscans = len(h5file)
            scan_range = generate_range(start_scan, end_scan, nscans + 1)

            first_scan_name = list(h5file.keys())[0]
            nimages, *detector_shape = h5file[
                f"{first_scan_name}/measurement/{detector_name}"
            ].shape
            image_range = list(generate_range(start_image, end_image, nimages))

            curr_sum = numpy.zeros(detector_shape)
            curr_monitor = 0
            curr_nb_images = 0

            with h5py.File(output_file, "a") as output:
                entry = output.require_group(output_entry)
                entry.attrs["NX_class"] = "NXentry"
                entry.attrs["default"] = output_process
                sum_process = entry.create_group(output_process)
                sum_process.attrs["NX_class"] = "NXprocess"
                sum_process.attrs["default"] = "results"
                results = sum_process.create_group("results")
                results.attrs["NX_class"] = "NXdata"

                output_uris = []
                for scan_number in scan_range:
                    scan_images = h5file[f"{scan_number}.1/measurement/{detector_name}"]
                    monitor_data = (
                        h5file[f"{scan_number}.1/measurement/{monitor_name}"]
                        if monitor_name
                        else None
                    )
                    assert isinstance(scan_images, h5py.Dataset)

                    for image_number in image_range:
                        curr_sum += scan_images[image_number]
                        if monitor_data:
                            curr_monitor = curr_monitor + monitor_data[image_number]
                        curr_nb_images += 1

                        if curr_nb_images == step:
                            dset = save_sum(
                                results,
                                name=f"Scan{scan_number}-Images{image_number - curr_nb_images + 1}-{image_number}",
                                data=curr_sum,
                                nb_images=curr_nb_images,
                                monitor=curr_monitor,
                            )
                            output_uris.append(f"{output_file}::{dset.name}")

                            # Move to next sum
                            curr_sum = numpy.zeros(detector_shape)
                            curr_monitor = 0
                            curr_nb_images = 0

                    if curr_nb_images > 0:
                        dset = save_sum(
                            results,
                            name=f"Sum_{len(output_uris)}",
                            data=curr_sum,
                            nb_images=curr_nb_images,
                            monitor=curr_monitor,
                        )
                        output_uris.append(f"{output_file}::{dset.name}")

        self.outputs.output_uris = output_uris
