import os
from contextlib import contextmanager

try:
    from bliss import setup_globals
    from bliss.common.logtools import user_info
except ImportError:
    setup_globals = None
    user_info = print

from ..streamline.scanner import StreamlineScanner
from .optimize_exposure import optimize_exposure
from ..persistent import ParameterInfo


class Id31StreamlineScanner(
    StreamlineScanner,
    parameters=[
        ParameterInfo("optimize_exposure", category="exposure/attenuator"),
        ParameterInfo("optimize_pixel_value", category="exposure/attenuator"),
        ParameterInfo("optimize_nb_frames", category="exposure/attenuator"),
        ParameterInfo("optimize_max_exposure_time", category="exposure/attenuator"),
        ParameterInfo("attenuator_name", category="names"),
        ParameterInfo("newflat", category="Flat-field"),
        ParameterInfo("oldflat", category="Flat-field"),
    ],
):
    def __init__(self):
        super().__init__()
        self._set_parameter_default("detector_name", "p3")
        self._set_parameter_default("attenuator_name", "atten")
        self._set_parameter_default("sample_changer_name", "streamline_sc")
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_ocl_gpu",
                "integrator_name": "sigma_clip_ng",
                "extra_options": {"max_iter": 3, "thres": 0},
                "error_model": "azimuthal",  # hybrid gives weird results
                "nbpt_rad": 4096,
                "unit": "q_nm^-1",
            },
        )
        self._set_parameter_default("optimize_exposure", False)
        self._set_parameter_default("optimize_pixel_value", 1e5)
        self._set_parameter_default("optimize_nb_frames", 3)
        self._set_parameter_default("optimize_max_exposure_time", 4)

    def _get_scan_metadata(self) -> dict:
        return dict()

    @contextmanager
    def run_context(self):
        setup_globals.shopen()
        with super().run_context():
            yield

    def measure_sample(self, count_time: float = 1, *args, **kwargs):
        att_value = None
        if self.optimize_exposure:
            detector = getattr(setup_globals, self.detector_name)
            attenuator = getattr(setup_globals, self.attenuator_name)
            att_value = attenuator.bits
            count_time = optimize_exposure(
                detector,
                tframe=0.2,
                default_att_position=None,
                desired_counts=self.optimize_pixel_value,
                dynamic_range=1 << 20,
                min_counts_per_frame=100,
                nframes_measure=1,
                nframes_default=self.optimize_nb_frames,
                reduce_desired_deviation=True,
                expose_with_integral_frames=False,
            )
            count_time = min(count_time, self.optimize_max_exposure_time)
        try:
            return super().measure_sample(count_time, *args, **kwargs)
        finally:
            if att_value is not None:
                setup_globals.att(att_value)

    def init_workflow(
        self, with_calibration: bool = False, flatfield: bool = True
    ) -> None:
        wd = "/users/opid31/ewoks/resources/workflows"
        if flatfield:
            if with_calibration:
                self.workflow = os.path.join(wd, "streamline_with_calib_with_flat.json")
            else:
                self.workflow = os.path.join(
                    wd, "streamline_without_calib_with_flat.json"
                )
        else:
            if with_calibration:
                self.workflow = os.path.join(wd, "streamline_with_calib.json")
            else:
                self.workflow = os.path.join(wd, "streamline_without_calib.json")

        user_info(f"Active data processing workflow: {self.workflow}")

    def _job_arguments(self, scan_info, processed_metadata: dict):
        args, kwargs = super()._job_arguments(scan_info, processed_metadata)
        inputs = kwargs["inputs"]
        inputs.append(
            {
                "task_identifier": "FlatFieldFromEnergy",
                "name": "newflat",
                "value": self.newflat,
            }
        )
        inputs.append(
            {
                "task_identifier": "FlatFieldFromEnergy",
                "name": "oldflat",
                "value": self.oldflat,
            }
        )
        energy = getattr(setup_globals, self.energy_name).position
        inputs.append(
            {
                "task_identifier": "FlatFieldFromEnergy",
                "name": "energy",
                "value": energy,
            }
        )
        return args, kwargs
