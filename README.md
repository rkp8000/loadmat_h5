# loadmat_h5
Function to load MATLAB .mat files stored as v7.3 or greater (i.e. in hdf5 format):

Use as:

`data = loadmat_h5('my_data_file.mat')`

You can copy and paste the loadmat_h5 function from `loadmat_h5.py`, or import it with `from loadmat_h5 import loadmat_h5`

(note: this requires the library h5py, which you can install via `conda install h5py` if using Anaconda or via `pip install h5py` if not using Anaconda)

See example usage in [loadmat_h5.ipynb](https://github.com/rkp8000/loadmat_h5/blob/master/loadmat_h5.ipynb).

This is a function equivalent to scipy's `loadmat` for when you get the following error using the latter:
```
---------------------------------------------------------------------------
NotImplementedError                       Traceback (most recent call last)
<ipython-input-16-200704b4a286> in <module>
      1 from scipy.io import loadmat
----> 2 loadmat(FILE)

~/miniconda3/envs/sci/lib/python3.6/site-packages/scipy/io/matlab/mio.py in loadmat(file_name, mdict, appendmat, **kwargs)
    215     variable_names = kwargs.pop('variable_names', None)
    216     with _open_file_context(file_name, appendmat) as f:
--> 217         MR, _ = mat_reader_factory(f, **kwargs)
    218         matfile_dict = MR.get_variables(variable_names)
    219 

~/miniconda3/envs/sci/lib/python3.6/site-packages/scipy/io/matlab/mio.py in mat_reader_factory(file_name, appendmat, **kwargs)
     76         return MatFile5Reader(byte_stream, **kwargs), file_opened
     77     elif mjv == 2:
---> 78         raise NotImplementedError('Please use HDF reader for matlab v7.3 files')
     79     else:
     80         raise TypeError('Did not recognize version %s' % mjv)

NotImplementedError: Please use HDF reader for matlab v7.3 files
```
