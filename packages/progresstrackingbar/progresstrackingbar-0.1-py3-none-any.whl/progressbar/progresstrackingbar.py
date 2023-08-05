import atexit
import inspect
from tqdm import tqdm

def track_script_progress():
    """
    Tracks the progress of the calling script using `tqdm`.
    """
    def show_status(progress):
        print(f"Progress: {progress}%")

    frame = inspect.currentframe().f_back
    _, _, total_lines, _, _ = inspect.getframeinfo(frame)

    pbar = tqdm(total=total_lines, desc="Script Progress")
    atexit.register(lambda: pbar.close())

    for i, line in enumerate(frame.f_code.co_code.splitlines()):
        pbar.update(1)
        show_status(int((i + 1) / total_lines * 100))
        frame.f_globals['__builtins__']['_'] = None

        # Disable the progress bar temporarily while waiting for user input
        if input_waiting():
            pbar.close()
            input_str = input()
            pbar = tqdm(total=total_lines - i - 1, desc="Script Progress")
            pbar.update(i+1)

        exec(line, frame.f_globals, frame.f_locals)

def input_waiting():
    """
    Returns True if there is input waiting on the console, False otherwise.
    """
    import select
    import sys

    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])