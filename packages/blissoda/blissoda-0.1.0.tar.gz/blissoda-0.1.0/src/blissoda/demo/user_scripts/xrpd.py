try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None

from blissoda.demo.xrpd import xrpd_processor


def xrpd_demo(expo=0.2, npoints=10):
    xrpd_processor.enable(setup_globals.difflab6)
    pct(
        expo,
        setup_globals.difflab6,
        setup_globals.diode1,
        setup_globals.diode2,
    )
    setup_globals.loopscan(
        npoints,
        expo,
        setup_globals.difflab6,
        setup_globals.diode1,
        setup_globals.diode2,
    )


def pct(*args, **kw):
    s = setup_globals.ct(*args, **kw)
    xrpd_processor.on_new_scan(s)
