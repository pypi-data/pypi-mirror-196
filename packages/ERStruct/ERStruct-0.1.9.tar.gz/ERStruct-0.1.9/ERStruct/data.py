import os
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

# Import package
import numpy as np
import pkg_resources

class Gene500:
    def download(self):
        data1 = pkg_resources.resource_string(__name__, 'data/char21.npy')
        data2 = pkg_resources.resource_string(__name__, 'data/char22.npy')
        np.save('sample_data/char21.npy', data1)
        np.save('sample_data/char22.npy', data2)



