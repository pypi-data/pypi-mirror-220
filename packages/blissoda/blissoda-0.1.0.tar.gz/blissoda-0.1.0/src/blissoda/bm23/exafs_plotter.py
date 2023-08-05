from ..exafs.plotter import ExafsPlotter


class Bm23ExafsPlotter(ExafsPlotter):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default("workflow", "/users/opd23/ewoks/online.ows")
        self._set_parameter_default("_scan_type", "cont")
        self._counters.setdefault(
            "cont",
            {
                "mu_name": "mu_trans",
                "energy_name": "energy_cenc",
                "energy_unit": "keV",
            },
        )
        self._counters.setdefault(
            "step",
            {
                "mu_name": "mu_trans",
                "energy_name": "eneenc",
                "energy_unit": "keV",
            },
        )

    def _scan_type_from_scan(self, scan) -> str:
        if "exafs_step" in scan.name:
            return "step"
        else:
            return "cont"
