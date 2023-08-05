# Uses psutil to observe/log processes during a certain time

### pip install procobserver

```python
from procobserver import observe_procs
df = observe_procs(
    executables=("Vpn.exe",), # list or tuple of exe files (not the whole path!)
    pids=(5800, 18166), # list or tuple of pids 
    pickle_output_path="f:\\picklefileobj.pkl", # If None, nothing will be saved to your HDD 
    sleeptime=0.2, # sleep between each scan 
	timeout=30, # If timeout is None, you have to press ctrl+c 
)
# Press ctrl+c to stop the observation
Out[2]: '\n^CStopping observation ...
df
Out[3]: 
0 num_handles  ...  aa_localtime
0         484  ...  1.678241e+09
1         604  ...  1.678241e+09
2         870  ...  1.678241e+09
3        1336  ...  1.678241e+09
4         419  ...  1.678241e+09
5         484  ...  1.678241e+09
6         604  ...  1.678241e+09
7         870  ...  1.678241e+09
8        1336  ...  1.678241e+09
9         419  ...  1.678241e+09
[10 rows x 28 columns]
```