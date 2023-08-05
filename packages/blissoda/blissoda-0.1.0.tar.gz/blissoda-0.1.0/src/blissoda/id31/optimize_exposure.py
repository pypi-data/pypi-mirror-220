from typing import Union, Optional
from contextlib import contextmanager
import numpy

try:
    from bliss import setup_globals
    from blissdata.data import lima_image
except ImportError:
    setup_globals = None
    lima_image = None

try:
    from id31 import attenuator as id31_attenuator
except ImportError:
    id31_attenuator = None


def set_attenuator_position(att_position: int) -> None:
    """SiO2 thickness (cm) ~= 1.25 * att_position"""
    setup_globals.atten.bits = att_position


def get_attenuator_position() -> int:
    return setup_globals.atten.bits


def get_energy_value() -> float:
    """keV"""
    return setup_globals.energy.position


@contextmanager
def diode_range_context():
    try:
        yield
    finally:
        setup_globals.att(setup_globals.atten.bits)


def optimize_exposure(
    detector,
    tframe: float = 0.2,
    default_att_position: Optional[int] = None,
    desired_counts: float = 1e5,
    dynamic_range: int = 1 << 20,
    min_counts_per_frame: float = 1000,
    nframes_measure: int = 1,
    nframes_default: int = 3,
    reduce_desired_deviation: bool = True,
    expose_with_integral_frames: bool = False,
) -> float:
    r"""Optimize the attenuator and return the optimal exposure time.

    * $I_m$: measured diffracted intensity (maximum pixel value)
    * $I_d$: desired diffracted intensity (maximum pixel value)
    * $R$: diffraction count rate (Hz, maximum pixel value per second)
    * $T(E,n)$: transmission at energy $E$ and attenuator position $n$

    .. math::

        \begin{align}
        I_m &= R * tframe * nframe_m * T(E,n_m) \\
        I_d &= R * tframe * nframe_d * T(E,n_d)
        \end{align}

    Solve the following equation to $n_d$ and $nframe_d$

    .. math::

        \frac{nframe_d * T(E,n_d)} = \frac{I_d * nframe_m * T(E,n_m)}{I_m}

    :param detector: lima detector object
    :param tframe: time of a single frame in accumulation mode
    :param default_att_position: start the optimization with this attenuator position
    :param desired_counts: we want to be close to this maximum pixel value
    :param dynamic_range: full well of the detector
    :param min_counts_per_frame: we need at least these counts to even start optimizing
    :param nframes_measure: number of frames used for optimization measurements
    :param nframes_default: try modify attenuators for this number of frames
    :param reduce_desired_deviation: reduce deviation from the desired counts
    :param expose_with_integral_frames: exposure time is n x frame time with n integral or not
    :returns: exposure time
    """
    Imax_perframe = dynamic_range - 1
    Id = desired_counts
    att_position_max = 31
    att_position_start = get_attenuator_position()

    with diode_range_context():
        if default_att_position is None:
            att_position = att_position_start
        else:
            att_position = default_att_position
            if att_position != att_position_start:
                set_attenuator_position(att_position)

        # Make sure we are BELOW the dynamic range of the detector
        Im_perframe = get_max_intensity_per_frame(detector, tframe, nframes_measure)
        while Im_perframe >= Imax_perframe and att_position < att_position_max:
            att_position += 1
            set_attenuator_position(att_position)
            Im_perframe = get_max_intensity_per_frame(detector, tframe, nframes_measure)
        if Im_perframe >= Imax_perframe:
            # We are at full attenuation and full dynamic range.
            # Decreasing the frame time would be an option but
            # ID31 keeps it fixed.
            return tframe

        # Make sure we have some counts to make the calculations
        # further on more reliable
        while Im_perframe < min_counts_per_frame and att_position:
            att_position -= 1
            set_attenuator_position(att_position)
            _prev = Im_perframe
            Im_perframe = get_max_intensity_per_frame(detector, tframe, nframes_measure)
            if Im_perframe >= Imax_perframe:
                att_position += 1
                Im_perframe = _prev
                break

        # Calculate all possible intensities with nframe_d=nframes_default
        #  I = R * tframe * nframes_default * T(E,n_d)
        transmissions = id31_attenuator.SiO2trans(
            get_energy_value(), numpy.arange(att_position_max + 1)
        )
        Rtframe = Im_perframe / transmissions[att_position]  # R * tframe
        Ichoices = Rtframe * nframes_default * transmissions
        att_desired = numpy.argmin(abs(Ichoices - Id))
        set_attenuator_position(att_desired)
        if att_desired != 0:
            if reduce_desired_deviation:
                # Reduce the deviation from Id by solving this to nframes_d
                #  I_d = R * tframe * nframes_d * T(E,n_d)
                nframe_d = Id / (Rtframe * transmissions[att_desired])
                if expose_with_integral_frames:
                    return _round_nframes(nframe_d) * tframe
                else:
                    return _round_nframes(nframe_d * tframe, ndecimals=1)
            return nframes_default * tframe

        # No attenuator: increase exposure time
        #  I_d = R * tframe * nframes
        nframe_d = Id / Rtframe
        if expose_with_integral_frames:
            return _round_nframes(nframe_d) * tframe
        return _round_nframes(nframe_d * tframe, ndecimals=1)


def _round_nframes(nframes: Union[float, int], ndecimals: int = 0) -> Union[float, int]:
    if ndecimals:
        m = 10**ndecimals
        return max(int(nframes * m + 0.5) / m, 1 / m)
    else:
        return max(int(nframes + 0.5), 1)


def get_max_intensity_per_frame(
    detector, tframe: float = 0.2, nframes: int = 1
) -> float:
    setup_globals.ct(tframe * nframes, detector)
    frame, _ = lima_image.read_video_last_image(detector.proxy)
    return frame.max() / nframes
