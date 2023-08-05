from . import controllers


def att(att_position):
    atten.bits = att_position


def ct(count_time: float = 1, *detectors, **kwargs):
    for detector in detectors:
        detector.ct(count_time, **kwargs)


source = controllers.Source()
energy = controllers.Mono(parent=source)
atten = controllers.Attenuator(parent=energy)
sample = controllers.DiffractingSample(parent=atten)
p3 = controllers.LimaDetector(parent=sample)
