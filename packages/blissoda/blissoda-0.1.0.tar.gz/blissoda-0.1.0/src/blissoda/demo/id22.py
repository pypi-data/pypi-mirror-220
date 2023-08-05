from pprint import pprint

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None
from ..id22.stscan_processor import StScanProcessor


class DemoStScanProcessor(StScanProcessor):
    def __init__(self) -> None:
        super().__init__(
            convert_workflow="/tmp/demo/convert.json",
            rebinsum_workflow="/tmp/demo/rebinsum.json",
            extract_workflow="/tmp/demo/extract.json",
        )

    def _submit_job(self, workflow, inputs, **kw):
        print("\nSubmit workfow")
        print(workflow)
        print("Inputs:")
        pprint(inputs)
        print("Options:")
        pprint(kw)


if setup_globals is None:
    stscan_processor = None
else:
    stscan_processor = DemoStScanProcessor()
