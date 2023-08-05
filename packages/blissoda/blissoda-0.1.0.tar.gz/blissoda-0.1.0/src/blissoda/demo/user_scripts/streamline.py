from blissoda.demo.streamline import streamline_sc
from blissoda.demo.streamline import streamline_scanner


def streamline_demo(with_calibration=False):
    # Nothing loaded and 2 holders in the tray:
    streamline_scanner.eject()
    streamline_sc.fill_tray(2)

    # Initialize workflow with or without calibration
    streamline_scanner.init_workflow(with_calibration=with_calibration)
    if with_calibration:
        streamline_scanner.calib(0.1)

    # Measure all holders
    streamline_scanner.run(0.1)
