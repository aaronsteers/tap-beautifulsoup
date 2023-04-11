from __future__ import annotations

import subprocess
from pathlib import Path


def run_cmd(cmd, verbose=False, *args, **kwargs):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


def download(url: str, download_folder: Path | str = "output", verbose: bool = False):
    cmd = f"wget --recursive --timestamping --directory-prefix={download_folder} {url}"
    run_cmd(cmd, verbose=verbose)
