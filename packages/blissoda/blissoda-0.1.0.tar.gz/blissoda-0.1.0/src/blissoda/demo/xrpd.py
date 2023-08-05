import numpy
import json
from typing import Optional, List

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None

from ..xrpd.processor import XrpdProcessor
from ..persistent import ParameterInfo


def energy_wavelength(x):
    """keV to m and vice versa"""
    return 12.398419843320026 * 1e-10 / x


_DEFAULT_CALIB = {
    "dist": 5e-2,  # 5 cm
    "poni1": 10e-2,  # 10 cm
    "poni2": 10e-2,  # 10 cm
    "rot1": numpy.radians(10),  # 10 deg
    "rot2": 0,  # 0 deg
    "rot3": 0,  # 0 deg
    "wavelength": energy_wavelength(12),  # 12 keV
    "detector": "Pilatus1M",
}


class DemoXrpdProcessor(
    XrpdProcessor,
    parameters=[
        ParameterInfo("config_filename", category="PyFai"),
        ParameterInfo("integration_options", category="PyFai"),
    ],
):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default("lima_names", ["difflab6"])
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_cython",
                "nbpt_rad": 4096,
                "radial_range_min": 1,
                "unit": "q_nm^-1",
            },
        )
        self._ensure_config_filename()

    def get_integrate_inputs(
        self, scan, lima_name: str, task_identifier: str
    ) -> List[dict]:
        self._ensure_config_filename()
        inputs = super().get_integrate_inputs(scan, lima_name, task_identifier)
        inputs.append(
            {"task_identifier": task_identifier, "name": "demo", "value": True}
        )
        return inputs

    def _ensure_config_filename(self):
        if self.config_filename:
            return
        cfgfile = "/tmp/test.json"
        poni = _DEFAULT_CALIB
        with open(cfgfile, "w") as f:
            json.dump(poni, f)
        self.config_filename = cfgfile

    def get_config_filename(self, lima_name: str) -> Optional[str]:
        return self.config_filename

    def get_integration_options(self, lima_name: str) -> Optional[dict]:
        return self.integration_options.to_dict()


if setup_globals is None:
    xrpd_processor = None
else:
    try:
        xrpd_processor = DemoXrpdProcessor()
    except ImportError:
        xrpd_processor = None
