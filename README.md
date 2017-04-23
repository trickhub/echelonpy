# echelonpy
Converts Schwinn MPower Echelon csv output to Garmin compatible tcx

## Usage
### Shell
```
cd echelonpy
python setup.py install
echelonpy /path/to/echelon.csv
```
### Module
```
from echelonpy import reader
reader.read('/path/to/echelon.csv')
```
