from contextlib import ExitStack
from contextlib import contextmanager
from unittest.mock import patch

from . import setup_globals
from . import lima_image
from . import attenuator


@contextmanager
def mock_id31():
    with ExitStack() as stack:
        ctx = patch("blissoda.id31.optimize_exposure.setup_globals", new=setup_globals)
        stack.enter_context(ctx)
        ctx = patch("blissoda.id31.optimize_exposure.id31_attenuator", new=attenuator)
        stack.enter_context(ctx)
        ctx = patch("blissoda.id31.optimize_exposure.lima_image", new=lima_image)
        stack.enter_context(ctx)
        yield
