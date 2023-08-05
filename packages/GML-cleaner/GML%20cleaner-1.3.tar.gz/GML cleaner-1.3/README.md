# GML cleaner
Python package to clean gml files. With this package, you can:
- read gml files as xml files (not as geo files with e.g. fiona)
- read the schema file that contains the meta data (usually a .xsd or .gfs file)
- replace commas by points in float properties
- change the datatype of properties (works only for .xsd files)
- save the changed gml and schema file

Usually, gml file are read by packages such as GeoPandas or Fiona. Yet, this package accesses the raw data directly, which the geo packages cannot do.
# Installation
```sh
pip install gml-cleaner
```

# Usage

```python
from clean_gml.gml import Gml

# set example file path
filepath = 'example.gml'

# optional: use dictionary to change the datatype of one or more properties
datatype_changes = {'PROPERTY': 'xsd:float'}

# instantiate the Gml class. It will automatically load the corresponding .xsd schema file
gml = Gml(filepath)
# optional: change datatypes
gml.datatype_changes(changes=datatype_changes)
# replace commas by dots and set number of decimals (default is 2)
gml.replace_commas(ndigits=3)
# save files
gml.save()  # saves files in new directory 'adjustud/'
```