import numpy
import json
from contextlib import contextmanager

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None

from ..streamline.scanner import StreamlineScanner


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


class DemoStreamlineScanner(StreamlineScanner):
    def __init__(self):
        super().__init__()
        self._set_parameter_default("detector_name", "difflab6")
        self._set_parameter_default("calibrant", "LaB6")
        self._set_parameter_default("sample_changer_name", "streamline_sc")
        self._set_parameter("image_slice", "0,0:-1,0:-1")
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_cython",
                "integrator_name": "sigma_clip_ng",
                "extra_options": {"max_iter": 3, "thres": 0},
                "error_model": "azimuthal",  # hybrid gives weird results
                "nbpt_rad": 4096,
                "unit": "q_nm^-1",
            },
        )

    def measure_sample(self, *args, **kwargs):
        return setup_globals.sct(*args, setup_globals.difflab6, **kwargs)

    def calib(self, *args, sample_index=0, **kwargs):
        return super().calib(*args, sample_index=sample_index, **kwargs)

    def init_workflow(self, with_calibration: bool = True):
        self._ensure_pyfai_config()
        return super().init_workflow(with_calibration=with_calibration)

    def _ensure_pyfai_config(self):
        if self.pyfai_config:
            return
        cfgfile = "/tmp/test.json"
        poni = _DEFAULT_CALIB
        with open(cfgfile, "w") as f:
            json.dump(poni, f)
        self.pyfai_config = cfgfile

    @contextmanager
    def run_context(self):
        yield

    @property
    def sample_changer(self):
        return streamline_sc

    def _job_arguments(self, *args, **kw):
        args, kwargs = super()._job_arguments(*args, **kw)
        kwargs["inputs"].append(
            {"task_identifier": "Integrate1D", "name": "demo", "value": True}
        )
        return args, kwargs

    def _get_workflow_upload_parameters(self, *args) -> None:
        return None


class MockSampleChanger:
    def __init__(self) -> None:
        self._vibration_speed = 0
        self._translation = MockSampleTranslation()
        self._nholes = 3
        self._nholders = 2
        self._loaded = False

    def fill_tray(self, n=2):
        self._nholders = n

    def qr_read(self):
        return f"lab6_{self.translation.position}"

    def select_sample(self, sample_index):
        self.translation.position = sample_index
        return self.qr_read()

    def select_sample_without_qr(self, sample_index):
        return self.select_sample(sample_index)

    def iterate_samples(self, sample_indices=None):
        if not sample_indices:
            sample_indices = range(self._nholes)
        for i in sample_indices:
            self.translation.position = i
            yield self.qr_read()

    def iterate_samples_without_qr(self, sample_indices=None):
        yield from self.iterate_samples(sample_indices=sample_indices)

    def eject_old_baguette(self):
        self._nholders = max(self._nholders - 1, 0)
        self._loaded = False
        self.translation.position = 20

    def load_baguette_with_homing(self):
        self._loaded = True
        self.translation.position = 0

    def has_remaining_baguettes(self):
        return bool(self._nholders)

    @property
    def number_of_remaining_baguettes(self):
        return self._nholders

    @property
    def translation(self):
        return self._translation

    @property
    def vibration_speed(self):
        return self._vibration_speed

    @vibration_speed.setter
    def vibration_speed(self, speed):
        self._print("SETTING VIBRATION SPEED TO", speed)
        if speed < 0 or speed > 100:
            raise RuntimeError(
                "Speed for the fluidization system out of range (0-100, as in %)"
            )
        self._vibration_speed = speed


class MockSampleTranslation:
    def __init__(self) -> None:
        self._position = 0

    def on(self):
        pass

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        print("Move streamline_translation from", self._position, "to", value)
        self._position = value


if setup_globals is None:
    streamline_scanner = None
    streamline_sc = None
    streamline_translation = None
else:
    streamline_scanner = DemoStreamlineScanner()
    streamline_sc = MockSampleChanger()
    streamline_translation = MockSampleTranslation()
