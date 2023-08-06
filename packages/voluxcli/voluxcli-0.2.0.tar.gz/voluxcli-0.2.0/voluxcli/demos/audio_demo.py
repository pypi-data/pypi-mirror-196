from volux import VoluxDemo


class AudioDemo(VoluxDemo):
    id = "audio"
    description = (
        "Visualize the loudness of your default recording device in the terminal."
    )
    DEV__requirements = [
        {"distribution_name": "voluxaudio", "version_requirement": ">=0.8.0"},
        {"distribution_name": "voluxexamplemodule", "version_requirement": ">=0.10.0"},
        {"distribution_name": "numpy"},
    ]

    @staticmethod
    def main():
        # REQUIRED MODULES:
        # - voluxaudio

        # built in
        from time import sleep
        from typing import Any

        # site
        from voluxaudio import VoluxAudioStream
        from voluxexamplemodule import VoluxMultiply, VoluxCliBar
        import numpy as np

        # -----------------
        # --- constants ---
        # -----------------
        AMP_MULTIPLIER = 0.01
        LOOP_HZ = 60
        CHUNK_SIZE = 140
        BUFFER_WINDOW_SIZE_IN_SAMPLES = 1024

        # -----------------
        # --- functions ---
        # -----------------
        def average_audio_data(audio_data: bytes, frame_count: int) -> Any:
            """Take audio data and return a single normalized value."""
            avg = np.linalg.norm(audio_data) / frame_count
            return avg

        # NOTE: we're using buffering, so this doesn't need to do anything
        def on_data(*args, **kwargs):
            return

        # --------------
        # --- script ---
        # --------------

        # TODO: ask user if they want to test if their computer's volume affects visualization
        # ... and if they respond yes display a test bar and play a sine wave of a consistent
        # ... amplitude and frequency and check if visualization is affected when volume changes.
        # ... If it is affected, inform user of results and request they max their volume for best
        # ... experience (optional of course), if it isn't affected, allow them to press a given
        # ... key to continue and let them know whatever output is working great and any volume
        # ... will be okay

        # Example of a 'source' Volux module
        with VoluxAudioStream(
            on_data=on_data,
            chunk_size=CHUNK_SIZE,
            buffer_size_in_seconds=1,
        ) as stream:
            # Example of a 'transformer' Volux module
            with VoluxMultiply(AMP_MULTIPLIER) as vlx_mult:
                # Example of a 'destination' Volux module
                with VoluxCliBar() as vlx_clibar:
                    while True:
                        samples = stream.buffer[-BUFFER_WINDOW_SIZE_IN_SAMPLES:]
                        amp = average_audio_data(samples, CHUNK_SIZE)
                        amp = min(int(vlx_mult.multiply(amp)), 100)
                        vlx_clibar.print(
                            amp,
                            max_segments=100,
                            left_fill="/",
                            level_char="#",
                        )
                        sleep(1 / LOOP_HZ)


if __name__ == "__main__":
    AudioDemo.main()
