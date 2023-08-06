# Voluxaudio

---

☠️ **EXPERIMENTAL:** - Beware all ye who enter here ☠️

---

### Todo List

- [x] Get simple `VoluxAudioStream` class working
- [x] Make `VoluxAudioStream` class highly configurable
- [x] Add basic example to documentation
- [ ] Add basic documentation
- [ ] Add more examples to documentation

### VoluxAudioStream Example

#### Summary

Draws a bar in your terminal based on a simple approximation of the amplitude (i.e. loudness) of the sound coming from your system's default recording device (microphone or computer/desktop audio).

![Voluxaudio Amplitude Example](assets/voluxaudio-amplitude-example.gif)

#### Example Code

```python
from voluxaudio import VoluxAudioStream
import numpy as np
from time import sleep

# call this every time new samples gathered
def on_data(*args, **kwargs):
    return

# open an audio stream with buffering enabled
with VoluxAudioStream(
    on_data=on_data,
    chunk_size=2048,
    channels=2,
    buffer_size_in_seconds=2,
) as audio_stream:

    # repeat until script stopped
    while True:

        # weakly approximate amplitude
        samples = audio_stream.buffer
        sample_count = len(samples)
        samples_per_channel = np.swapaxes(samples, 0, 1)
        L_channel_e = np.average(np.abs(samples_per_channel[0][-2048:])) / sample_count
        R_channel_e = np.average(np.abs(samples_per_channel[1][-2048:])) / sample_count
        e = (L_channel_e + R_channel_e) / 2

        # print bar
        print(f"{e:<3.3f} " + int(e*100) * '|')

        # wait ~50ms
        sleep(1 / 20)
```

#### Information

- Please note that this is only a simple example and **much more complex audio processing is easily achievable**.
- A bar is printed every 50ms that gets longer/shorter depending on the approximated amplitude.
- Whether your system *volume* (not amplitude) affects results depends on your system, so it's best to test pausing/unpausing your music if you're using computer/desktop audio instead of a microphone.
- This example uses buffering as a `buffer_size_in_seconds` value is specified.
