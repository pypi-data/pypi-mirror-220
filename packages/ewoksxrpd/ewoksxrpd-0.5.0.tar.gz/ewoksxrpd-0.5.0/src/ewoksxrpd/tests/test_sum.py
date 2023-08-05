from ewoksorange.tests.utils import execute_task
from ewoksxrpd.tasks.sum import SumImages
import pytest
import os.path


@pytest.mark.parametrize("monitor_name", ("mon", None))
def test_sum(tmpdir, bliss_perkinelmer_scan, monitor_name):
    inputs = {
        "filename": str(bliss_perkinelmer_scan),
        "detector_name": "perkinelmer",
        "output_file": str(tmpdir / "output.h5"),
        "start_scan": 2,
        "end_image": 10,
        "end_scan": 2,
        "monitor_name": monitor_name,
    }

    outputs = execute_task(
        SumImages,
        inputs=inputs,
    )

    assert os.path.isfile(str(tmpdir / "output.h5"))
    assert len(outputs["output_uris"]) > 0
