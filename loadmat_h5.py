import h5py
import numpy as np

Dataset = h5py._hl.dataset.Dataset
Group = h5py._hl.group.Group
Reference = h5py.h5r.Reference


def loadmat_h5(file_name):
    '''Loadmat equivalent for -v7.3 or greater .mat files, which break scipy.io.loadmat'''
    
    def deref_s(s, f, verbose=False):  # dereference struct
        keys = [k for k in s.keys() if k != '#refs#']
        
        if verbose:
            print(f'\nStruct, keys = {keys}')

        d = {}

        for k in keys:
            v = s[k]

            if isinstance(v, Group):  # struct
                d[k] = deref_s(v, f, verbose=verbose)
            elif isinstance(v, Dataset) and isinstance(np.array(v).flat[0], Reference):  # cell
                d[k] = deref_c(v, f, verbose=verbose)
            elif isinstance(v, Dataset) and v.dtype == 'uint16':
                d[k] = ''.join(np.array(v).view('S2').flatten().astype(str))
                if verbose:
                    print(f'String, chars = {d[k]}')
            elif isinstance(v, Dataset):  # numerical array
                d[k] = np.array(v).T
                if verbose:
                    print(f'Numerical array, shape = {d[k].shape}')

        return d

    def deref_c(c, f, verbose=False):  # dereference cell
        n_v = c.size
        shape = c.shape

        if verbose:
            print(f'\nCell, shape = {shape}')

        a = np.zeros(n_v, dtype='O')

        for i in range(n_v):
            v = f['#refs#'][np.array(c).flat[i]]

            if isinstance(v, Group):  # struct
                a[i] = deref_s(v, f, verbose=verbose)
            elif isinstance(v, Dataset) and isinstance(np.array(v).flat[0], Reference):  # cell
                a[i] = deref_c(v, f, verbose=verbose)
            elif isinstance(v, Dataset) and v.dtype == 'uint16':
                a[i] = ''.join(np.array(v).view('S2').flatten().astype(str))
                if verbose:
                    print(f'String, chars = {a[i]}')
            elif isinstance(v, Dataset):  # numerical array
                a[i] = np.array(v).T
                if verbose:
                    print(f'Numerical array, shape = {a[i].shape}')

        return a.reshape(shape).T
    
    with h5py.File(file_name, 'r+') as f:
        d = deref_s(f, f)
        
    return d