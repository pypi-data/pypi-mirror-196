from . import _np
from packaging import version

def rolling_window(a, window, step=1):
    if version.parse(_np.version.version) < version.parse('1.20.0'):
        # before numpy 1.20.0
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return _np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)[::step]
    else:
        # after numpy 1.20.0
        return _np.lib.stride_tricks.sliding_window_view(a, window)[::step]

def sig2frames(sig, frame_size, overlap=0, padding=True):
    assert 0<=overlap<frame_size
    step = frame_size - overlap
    slice_window = rolling_window(sig, frame_size, step)
    if padding:
        remain_data = sig[slice_window.shape[0]*step:]
        last_frame = _np.pad(remain_data, (0,frame_size-remain_data.size))
        slice_window = _np.vstack([slice_window, last_frame])
    return slice_window