import os
import sys

stdout = sys.stdout

if os.getenv("BEAM_SERIALIZE_MODE") is not None:
    sys.stdout = open(os.devnull, "w")


def print_config(*args, **kwargs):
    sys.stdout = stdout
    print(*args, **kwargs)
    sys.stdout = open(os.devnull, "w")
