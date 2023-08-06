# useful resources:
# very useful discussion regarding chunk sizes: https://www.dataq.com/data-acquisition/general-education-tutorials/what-you-really-need-to-know-about-sample-rate.html
# real-time wave plotting: https://github.com/hnhaefliger/pyAudioGraph/blob/master/waves.py

# built in
from typing import Callable, Tuple, Any
from enum import Enum

# site
from volux import VoluxSource

import sounddevice as sd
import numpy as np
from numpy_ringbuffer import RingBuffer

# module
from .computer import get_samplerates

# -----------------
# --- constants ---
# -----------------

DEFAULT_CHUNK_SIZE = 140  # NOTE(Denver): lowest possible frequency that can be accurately measured (unbuffered) is 45Hz
DEFAULT_CHANNEL_COUNT = 2  # HACK(Denver): this should be dynamic
# HACK(Denver): would be good if this was configurable,
# ... however it's important to note it has the potential
# ... to significantly bloat the projects codebase if it
# ... is configurable. The advantage to making this configurable
# ... would, _presumably_, be allowing for more or less accurate
# ... audio processing, which could help improve quality of
# ... visualization on powerful devices, and improve performance
# ... on devices that aren't as powerful such as a Raspberry Pi
AUDIO_STREAM_READ_DTYPE = np.int16

# --------------
# --- typing ---
# --------------

StreamCallbackType = Callable[
    [bytes, int, dict, int],
    Tuple[bytes, int],
]

# ---------------
# --- classes ---
# ---------------

class vaBitDepth(Enum):
    """Audio bit depth enumerable."""

    Int16 = {"dtype_write": np.int16, "dtype_read": np.int16}


class VoluxAudioStream(VoluxSource):
    """Class for managing an audio stream."""

    def __init__(
        self,
        on_data: StreamCallbackType,
        bit_depth: vaBitDepth = vaBitDepth.Int16,  # default: 16bit signed interger (-32768..+32768)
        chunk_size=DEFAULT_CHUNK_SIZE,  # arbitrary number of samples collected per chunk (on_data called once chunk_size reached)
        channels=DEFAULT_CHANNEL_COUNT,  # number of audio channels (cannot get from sounddevice, seems to always report 32 inputs and 32 outputs, which is presumably the max for the 'default' device)
        sample_rate_override=None,  # override total number of samples that can be taken every second (maximum value constrained by user's system configuration!)
        buffer_size_in_seconds=None,
    ):
        """
        See class docstring for more info.

        : param on_data : TODO(Denver): docstring desc. for this.
        : param chunk_size: arbitrary number of frames per sample, lower this value for more frequent callbacks
        """
        # ensure on_data is callable
        if not callable(on_data):
            raise TypeError("on_data must be callable")

        # set values used in callback in advance
        _buffer_write_dtype = bit_depth.value["dtype_write"]
        _buffer_read_dtype = bit_depth.value["dtype_read"]
        _channel_count = channels
        _sample_rate = (
            # use sample rate of default input device unless override specified
            get_samplerates()[0]
            if sample_rate_override is None
            else sample_rate_override
        )

        # set up audio buffer
        if buffer_size_in_seconds is not None:
            _capacity = int(buffer_size_in_seconds * _sample_rate)

            buffer = RingBuffer(
                capacity=_capacity,
                dtype=np.dtype((_buffer_read_dtype, _channel_count)),
            )

            buffer.extend(np.zeros((_capacity, _channel_count)))

            self.buffer = buffer

        def _get_stream_callback():
            """Return either a buffered or non-buffered stream callback depending on settings."""

            if buffer_size_in_seconds is None:
                def _stream_callback(in_data, frame_count, time_info, status_flags):
                    """
                    Sets up a stream callback that wraps on_data.
                    
                    This allows the on_data callback to be hot-swapped in a safe/controlled manner.
                    """
                    self._on_data(
                        in_data,
                        frame_count,
                        time_info,
                        status_flags,
                        _buffer_read_dtype,
                        _channel_count,
                        _sample_rate,
                    )
                return _stream_callback

            else:
                def _stream_callback(in_data, frame_count, time_info, status_flags):
                    """
                    Sets up a stream callback that wraps on_data.
                    
                    This allows the on_data callback to be hot-swapped in a safe/controlled manner.
                    """
                    # push in_data into ring buffer
                    self.buffer.extend(in_data)

                    self._on_data(
                        in_data,
                        frame_count,
                        time_info,
                        status_flags,
                        _buffer_read_dtype,
                        _channel_count,
                        _sample_rate,
                    )
                return _stream_callback

        # set attributes with instance args/kwargs
        self._on_data = on_data
        self._bit_depth = bit_depth
        self._buffer_write_dtype = _buffer_write_dtype
        self._buffer_read_dtype = _buffer_read_dtype
        self._chunk_size = chunk_size
        self._channel_count = _channel_count
        self._sample_rate = _sample_rate
        self._stream_callback = _get_stream_callback()
        self.sounddevice = sd

        # initialise superclass with relevant args/kwargs
        super().__init__(prepare=self.start, cleanup=self.stop)

    def start(self):
        self.stream = self.sounddevice.InputStream(
            samplerate=self._sample_rate,
            blocksize=self._chunk_size,
            channels=self._channel_count,
            dtype=self._buffer_write_dtype,  # TODO: check if this is actually meant to be 'read' not 'write' attribute
            callback=self._stream_callback,
        )
        self.stream.__enter__()
        return True

    def stop(self):
        self.stream.__exit__()
        return True

    def update_callback(self, on_data: StreamCallbackType):
        self._on_data = on_data

    def __enter__(self):
        """Start stream."""
        self.start()
        return self

    def __exit__(
        self, exception_type: Any, exception_value: Any, traceback: Any
    ) -> Any:
        """Stop stream."""
        self.stop()
        # NOTE: WARNING! - don't return anything from this method!
        # ... Exceptions will be suppressed on exit!
