# anutils
ML and single cell analysis utils.  
## installation
```
pip install anutils
```
## usage
### general utils: `anutils.*`

e.g., reload module
```python
import sys
sys.path.append('/path/to/some/packaege/')
import some_package

# change some_package.sub_module.func, recursive reload needed
from anutils import rreload
rreload(some_package, max_depth=2)
```


### single cell utils: `anutils.scutils.*`

#### plotting

```python
from anutils import scutils as scu

# a series of embeddings grouped by disease status
scu.pl.embeddings(adata, basis='X_umap', groupby='disease_status', **kwargs) # kwargs for sc.pl.embedding

# enhanced dotplot with groups in hierarchical order
scu.pl.dotplot(adata, var_names, groupby, **kwargs) # kwargs for sc.pl.dotplot
```
#### cuda-accelerated scanpy functions
NOTE: to use these functions, you need to install rapids first. see [rapids.ai](https://rapids.ai/start.html) for details.
```python
from anutils.scutils import sc_cuda as cusc

# 10-100 times faster than scanpy leiden
cusc.sc.leiden(adata, resolution=0.5, key_added='leiden_0.5')

# 10-100 times faster than scib silhouette
cusc.sb.silhouette(adata, group_key, embed)
```

## machine learning utils:
```python
import anutils.mlutils as ml

# to be added
```
