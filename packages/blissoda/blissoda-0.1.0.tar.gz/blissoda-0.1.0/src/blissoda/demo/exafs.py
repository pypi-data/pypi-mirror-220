import os

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None
from ..exafs.plotter import ExafsPlotter
from ..resources.exafs import RESOURCE_ROOT


class DemoExafsPlotter(ExafsPlotter):
    def __init__(self) -> None:
        super().__init__()
        self._set_parameter_default(
            "workflow", os.path.join(RESOURCE_ROOT, "exafs.ows")
        )
        self._set_parameter_default("_scan_type", "any")
        self._counters.setdefault(
            "any",
            {
                "mu_name": "mu",
                "energy_name": "energy",
                "energy_unit": "eV",
            },
        )

    def _scan_type_from_scan(self, scan) -> str:
        return "any"

    def run(self, expo=0.003):
        e0 = 8800
        e1 = 9600
        scan = setup_globals.ascan(
            setup_globals.energy,
            e0,
            e1,
            (e1 - e0) * 2,
            expo,
            setup_globals.mu,
            run=False,
        )
        super().run(scan)


if setup_globals is None:
    exafs_plotter = None
else:
    exafs_plotter = DemoExafsPlotter()
    exafs_plotter.refresh_period = 0.5
