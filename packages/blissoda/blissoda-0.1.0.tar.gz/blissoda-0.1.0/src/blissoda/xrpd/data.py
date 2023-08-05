from typing import Tuple, List, Optional, Callable
import json
import numpy
from silx.io import h5py_utils
from silx.utils.retry import RetryError
from silx.utils.retry import RetryTimeoutError

try:
    from blissdata import settings
    from blissdata.data.events.channel import ChannelDataEvent
    from blissdata.streaming import DataStream
except ImportError:
    try:
        from bliss.config import settings
        from bliss.data.events.channel import ChannelDataEvent
        from bliss.config.streaming import DataStream
    except ImportError:
        settings = None
        ChannelDataEvent = None
        DataStream = None


def loads(v):
    if not isinstance(v, dict):
        return json.loads(v)
    return v


def dumps(v):
    return json.dumps(v)


def get_redis_store(redis_key: str) -> settings.OrderedHashObjSetting:
    return settings.OrderedHashObjSetting(
        redis_key, read_type_conversion=loads, write_type_conversion=dumps
    )


def add_plot(
    redis_store: settings.OrderedHashObjSetting,
    scan_name: str,
    lima_name: str,
    ct: bool,
    xlabel: str,
    xvalues: numpy.ndarray,
    hdf5_url: Optional[str] = None,
) -> Tuple[str, dict]:
    plot_key = f"{scan_name}:{lima_name}"
    data_key = f"{redis_store.name}:{plot_key}"
    if hdf5_url is None:
        hdf5_url = ""
    plot_info = {
        "scan_name": scan_name,
        "lima_name": lima_name,
        "xlabel": xlabel,
        "ct": ct,
        "data_key": data_key,
        "hdf5_url": hdf5_url,
    }
    redis_store[plot_key] = plot_info
    datastream = DataStream(data_key)
    datastream.add_event(_create_event(xvalues))
    return plot_key, plot_info


def remove_plots(
    redis_store: settings.OrderedHashObjSetting,
    max_len: int,
    remove_from_flint: Callable,
) -> List[Tuple[str, dict]]:
    all_plots = list(redis_store.items())
    if max_len > 0:
        remove = list()
        keep_scans = set()
        for plot_key, plot_info in all_plots[::-1]:
            scan_name = plot_info["scan_name"]
            if len(keep_scans) == max_len and scan_name not in keep_scans:
                remove.append((plot_key, plot_info))
            else:
                keep_scans.add(scan_name)
    else:
        remove = all_plots
    if remove:
        for plot_key, plot_info in remove:
            remove_from_flint(plot_key, plot_info)
            DataStream(plot_info["data_key"]).clear()
            redis_store.remove(plot_key)
    return remove


def add_data(plot_key: str, plot_info: dict, points: numpy.ndarray) -> str:
    datastream = DataStream(plot_info["data_key"])
    datastream.add_event(_create_event(points))
    return plot_key


def _create_event(data: numpy.ndarray) -> ChannelDataEvent:
    desc = {"shape": data.shape[1:], "dtype": data.dtype}
    return ChannelDataEvent(data, desc)


def get_curve_data(
    redis_store: settings.OrderedHashObjSetting, plot_key: str, **retry_options
) -> Tuple[Optional[numpy.ndarray], Optional[numpy.ndarray], dict]:
    plot_info = redis_store[plot_key]
    x = y = None
    datastream = DataStream(plot_info["data_key"])
    events = datastream.range(count=1)
    if not events:
        return x, y, plot_info
    x = decode_first_event(events)

    if plot_info["hdf5_url"]:
        try:
            y = get_data_from_file(plot_info["hdf5_url"], idx=-1, **retry_options)
        except RetryTimeoutError:
            y = None
    else:
        events = datastream.rev_range(count=1)
        if not events:
            return x, y, plot_info
        y = decode_first_event(events)
        if y.ndim == 2:
            y = y[-1]
    return x, y, plot_info


def get_image_data(
    redis_store: settings.OrderedHashObjSetting,
    plot_key: str,
    data: Optional[numpy.ndarray] = None,
    **retry_options,
) -> Tuple[Optional[numpy.ndarray], Optional[numpy.ndarray], dict]:
    plot_info = redis_store[plot_key]
    x = y = None
    datastream = DataStream(plot_info["data_key"])
    events = datastream.range()
    if not events:
        return x, y, plot_info
    x = decode_first_event(events)
    if plot_info["hdf5_url"]:
        if data is None:
            idx = tuple()
        else:
            idx = slice(len(data), None)
        try:
            y = get_data_from_file(plot_info["hdf5_url"], idx=idx, **retry_options)
        except RetryTimeoutError:
            y = None
        else:
            if data is not None:
                y = numpy.vstack([data, y])
    else:
        events = events[1:]
        if not events:
            return x, y, plot_info
        y = decode_all_events(events)
    return x, y, plot_info


def decode_first_event(events: List[Tuple[bytes, dict]]) -> numpy.ndarray:
    return ChannelDataEvent(raw=events[0][1]).data


def decode_all_events(events: List[Tuple[bytes, dict]]) -> numpy.ndarray:
    return ChannelDataEvent.merge(events).data


@h5py_utils.retry()
def get_data_from_file(hdf5_url: str, idx=tuple()):
    filename, dsetname = hdf5_url.split("::")
    with h5py_utils.File(filename) as root:
        try:
            return root[dsetname][idx]
        except KeyError as e:
            raise RetryError(str(e))
