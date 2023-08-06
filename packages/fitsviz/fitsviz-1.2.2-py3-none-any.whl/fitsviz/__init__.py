import atexit
from fitsviz.utils.cutils import create_dask_client
from fitsviz.utils.cutils import cleanup_dask_client
from fitsviz import detection
# Create the Dask Client when the package is imported
