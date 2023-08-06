import os
import sys

if os.getenv("BEAM_SERIALIZE") == "1":
    stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")

def print_config(*args, **kwargs):
    sys.stdout = stdout
    print(*args, **kwargs)
    sys.stdout = open(os.devnull, "w")