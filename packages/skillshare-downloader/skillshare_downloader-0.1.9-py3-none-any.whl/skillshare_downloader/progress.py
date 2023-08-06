import os
import subprocess
import sys
from ffmpeg import probe
from tqdm import tqdm

class ffmpegDown:
    def __init__(self, command, type):
        index_of_filepath = command.index("-i") + 1
        self._filepath = str(command[index_of_filepath])
        self._output_filepath = str(command[-1])
        self.type = type

        dirname = os.path.dirname(self._output_filepath)

        if dirname != "":
            self._dir_files = [file for file in os.listdir(dirname)]
        else:
            self._dir_files = [file for file in os.listdir()]

        self._can_get_duration = True

        try:
            self._duration_secs = round(float(probe(self._filepath)["format"]["duration"]), 1)
        except Exception:
            self._can_get_duration = False

        self._ffmpeg_args = command + ["-hide_banner", "-loglevel", "verbose"]

        if self._can_get_duration:
            self._ffmpeg_args += ["-progress", "pipe:1", "-nostats"]

    def run(self):

        process = subprocess.Popen(
            self._ffmpeg_args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )

        if self._can_get_duration:
            progress_bar = tqdm(total=round(self._duration_secs, 1), unit="s", dynamic_ncols=True, leave=False, desc=f'Downloading {self.type}')
            progress_bar.clear()
            previous_seconds_processed = 0

        try:
            while process.poll() is None:
                if self._can_get_duration:
                    ffmpeg_output = process.stdout.readline().decode()

                    if "out_time_ms" in ffmpeg_output:
                        seconds_processed = round(int(ffmpeg_output.strip()[12:]) / 1_000_000, 1)
                        seconds_increase = seconds_processed - previous_seconds_processed

                        # Ensure seconds_increase is always positive
                        seconds_increase = max(seconds_increase, 0)
                        progress_bar.update(seconds_increase)
                        previous_seconds_processed = seconds_processed

        except KeyboardInterrupt:
            progress_bar.close()
            process.kill()
            print("[KeyboardInterrupt] FFmpeg process killed. Exiting Better FFmpeg Progress.")
            sys.exit()

        except Exception as e:
            progress_bar.close()
            process.kill()
            print(f"[Error] {e}\nExiting Better FFmpeg Progress.")
            sys.exit()

        finally:
            progress_bar.close()
            progress_bar.clear()
