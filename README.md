# echelonpy
Converts Schwinn MPower Echelon csv output to Garmin compatible tcx

# Usage
### Shell
```
cd echelonpy
python setup.py install
echelonpy /path/to/echeclon.csv
```
### Module
```
from echelonpy import reader
reader.read('/path/to/echeclon.csv')
```
