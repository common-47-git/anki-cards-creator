import argparse
import os


def valid_path(path_str: str) -> str:
    """
    Validate that the directory for the given path exists and is writable.
    Used as the `type` argument in argparse.
    """
    save_dir = os.path.dirname(path_str) or "."
    if not os.path.exists(save_dir):
        raise argparse.ArgumentTypeError(f"Directory '{save_dir}' does not exist.")
    if not os.access(save_dir, os.W_OK):
        raise argparse.ArgumentTypeError(f"Directory '{save_dir}' is not writable.")
    return path_str
