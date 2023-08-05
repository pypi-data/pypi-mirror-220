"""Automatic pyfai integration for every scan with saving and plotting"""

from typing import Optional
from ..xrpd.processor import XrpdProcessor
from ..persistent import ParameterInfo


class Bm02XrpdProcessor(
    XrpdProcessor,
    parameters=[
        ParameterInfo("config_filename", category="PyFai"),
        ParameterInfo("integration_options", category="PyFai"),
    ],
):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default("config_filename", {"WOS": "", "D5": ""})
        self._set_parameter_default(
            "integration_options",
            {
                "WOS": {
                    "method": "no_csr_cython",
                    "nbpt_rad": 4096,
                    "unit": "q_nm^-1",
                },
                "D5": {
                    "method": "no_csr_cython",
                    "nbpt_rad": 4096,
                    "unit": "q_nm^-1",
                },
            },
        )

    def get_config_filename(self, lima_name: str) -> Optional[str]:
        try:
            return self.config_filename[lima_name]
        except KeyError:
            raise RuntimeError(
                f"Missing pyfai configuration file (poni or json) for '{lima_name}'"
            ) from None

    def get_integration_options(self, lima_name: str) -> Optional[dict]:
        try:
            return self.integration_options[lima_name]
        except KeyError:
            raise RuntimeError(
                f"Missing pyfai integration options for '{lima_name}'"
            ) from None
