# HErZ-HaPoMe

For using the `import_DAT` script, enter the following in a Jupyter-Notebook in the Vital Folder:

```python
import matplotlib.pyplot as plt
import xarray as xr

from import_DAT import get_data_from_dat_file
from import_DAT import get_data_from_folder

dat1_complete = get_data_from_folder("GEC_CL51_Testfiles")

```

It then can be plotted as follows:

```python
plt.figure().set_figwidth(15)
dat1_complete.plot()
plt.savefig("GEC_PLot.png")
```
