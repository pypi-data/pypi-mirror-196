# atflagger

A simple flagger for continuum UWL data. Flag persistent RFI first, then run this auto-flagger.

## Installation

Installing requires `pip` and `python3` (3.8 and up).

Stable version:
```
pip install atflagger
```

Latest version:
```
pip install git+https://github.com/AlecThomson/atflagger
```

## Usage
```
❯ atflagger -h
usage: atflagger [-h] [-i] [-b BEAM] [-s SIGMA] [-n N_WINDOWS] [-w] [-r REPORT] filenames [filenames ...]

atflagger - Automatic flagging of UWL data.

positional arguments:
  filenames             Input SDHDF file(s)

optional arguments:
  -h, --help            show this help message and exit
  -i, --inplace         Update flags in-place (default: create new file)
  -b BEAM, --beam BEAM  Beam label
  -s SIGMA, --sigma SIGMA
                        Sigma clipping threshold
  -n N_WINDOWS, --n-windows N_WINDOWS
                        Number of windows to use in box filter
  -w, --use-weights     Use weights table instead of flag table
  -r REPORT, --report REPORT
                        Optionally save the Dask (html) report to a file
```
