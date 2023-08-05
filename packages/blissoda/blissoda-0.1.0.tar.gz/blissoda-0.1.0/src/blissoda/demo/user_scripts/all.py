from blissoda.xrpd.processor import XrpdProcessor
from blissoda.exafs.plotter import ExafsPlotter
from blissoda.streamline.scanner import StreamlineScanner

from blissoda.bm23.exafs_plotter import Bm23ExafsPlotter
from blissoda.bm02.xrpd_processor import Bm02XrpdProcessor
from blissoda.id11.xrpd_processor import Id11XrpdProcessor
from blissoda.id31.xrpd_processor import Id31XrpdProcessor
from blissoda.id31.streamline_scanner import Id31StreamlineScanner

from blissoda.demo.exafs import exafs_plotter
from blissoda.demo.xrpd import xrpd_processor
from blissoda.demo.id22 import stscan_processor
from blissoda.demo.streamline import streamline_scanner

from blissoda.demo.user_scripts.exafs import exafs_demo
from blissoda.demo.user_scripts.id22 import id22_demo
from blissoda.demo.user_scripts.streamline import streamline_demo
from blissoda.demo.user_scripts.xrpd import xrpd_demo

try:
    from bliss import setup_globals
except ImportError:
    setup_globals = None


def all_print():
    _print_objects(exafs_plotter)
    _print_objects(xrpd_processor)
    _print_objects(stscan_processor)
    _print_objects(streamline_scanner)

    _print_objects(XrpdProcessor())
    _print_objects(ExafsPlotter())
    _print_objects(StreamlineScanner())

    _print_objects(Bm23ExafsPlotter())
    _print_objects(Bm02XrpdProcessor())
    _print_objects(Id11XrpdProcessor())
    _print_objects(Id31XrpdProcessor())

    _print_objects(Id31StreamlineScanner())


def all_demo():
    print()
    print("===================")
    setup_globals.newcollection("exafs")
    exafs_demo()

    print()
    print("===================")
    setup_globals.newcollection("id22")
    id22_demo()

    print()
    print("===================")
    setup_globals.newcollection("streamline")
    streamline_demo()

    print()
    print("===================")
    setup_globals.newcollection("xrpd")
    xrpd_demo()

    print()
    print("===================")
    setup_globals.newcollection()


def _print_objects(obj):
    print()
    print("===================")
    print(obj._parameters.name)
    print(obj.__info__())
