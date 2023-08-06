import os
import sys

stdout = sys.stdout

if os.getenv("BEAM_SERIALIZE") == "1":
    sys.stdout = open(os.devnull, "w")

def print_config(*args, **kwargs):
    sys.stdout = stdout
    print(*args, **kwargs)
    sys.stdout = open(os.devnull, "w")