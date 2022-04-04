"""Load, save and update json files."""
import os
import io
import json
from datetime import datetime


def save_json(filename, config):
    """Save configuration file as JSON.

    Parameters
    ----------
    filename : string
        Name of the configuration file to save.
    config : dict
        Dictionary of arguments to save.
    """
    # Ensure Python version compatibility
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str

    if filename:
        with io.open(filename, 'w', encoding='utf8') as f:
            str_ = json.dumps(config, indent=4, sort_keys=True,
                              separators=(',', ': '),  # Pretty printing
                              ensure_ascii=False)
            f.write(to_unicode(str_))


def load_json(filename):
    """Load configuration file as JSON.

    Parameters
    ----------
    filename : string
        Name of the configuration file to load.

    Returns
    -------
    config : dict
        Dictionary of config.
    """
    with open(filename) as f:
        # Load the configuration file :
        config = json.load(f)
    return config


def update_json(filename, update, backup=None):
    """Update a json file.

    Parameters
    ----------
    filename : str
        Full path to the json file.
    update : dict
        Dict for update.
    backup : str | None
        Backup folder if needed.
    """
    assert isinstance(update, dict)
    assert os.path.isfile(filename)
    config = load_json(filename)
    _backup_json(filename, backup)
    config.update(update)
    save_json(filename, config)


def _backup_json(filename, backup=None):
    if isinstance(backup, str):
        assert os.path.isfile(filename)
        assert os.path.exists(backup)
        # Load json file :
        config = load_json(filename)
        config_backup = config.copy()
        # Datetime :
        now = datetime.now()
        now_lst = [now.year, now.month, now.day, now.hour, now.minute,
                   now.second]
        now_lst = '_'.join([str(k) for k in now_lst])
        file, ext = os.path.splitext(os.path.split(filename)[1])
        file += now_lst + ext
        save_json(os.path.join(backup, file), config_backup)


def save_file(name, *arg, compress=False, **kwargs):
    """Save a file without carrying of extension.

    Parameters
    ----------
    name : string
        Full path to the file (could be pickle, mat, npy, npz, txt, json,
        xslx, csv).
    """
    name = safety_save(name)
    file_name, file_ext = os.path.splitext(name)
    if file_ext == '.pickle':  # Pickle
        import pickle
        with open(name, 'wb') as f:
            pickle.dump(kwargs, f)
    elif file_ext == '.mat':  # Matlab
        from scipy.io import savemat
        savemat(name, kwargs)
    elif file_ext == '.npy':  # Numpy (single array)
        import numpy as np
        np.save(name, *arg)
    elif file_ext == '.npz':  # Numpy (multi array)
        import numpy as np
        if compress:
            np.savez_compressed(name, kwargs)
        else:
            np.savez(name, kwargs)
    elif file_ext == '.json':  # JSON
        save_json(name, kwargs)
    elif file_ext == '.xlsx':  # JSON
        import pandas as pd
        assert isinstance(arg[0], pd.DataFrame)
        writer = pd.ExcelWriter(name)
        arg[0].to_excel(writer)
        writer.save()
    else:
        raise IOError("Extension %s not supported." % file_ext)


def load_file(name):
    """Load a file without carrying of extension.

    Parameters
    ----------
    name : string
        Full path to the file (could be pickle, mat, npy, npz, txt, json, xlsx,
        xls, csv).
    """
    assert os.path.isfile(name)
    file_name, file_ext = os.path.splitext(name)
    if file_ext == '.pickle':  # Pickle :
        import pickle
        return pd.read_pickle(name)
        # with open(name, "rb") as f:
        #     arch = pickle.load(f)
        # return arch
    elif file_ext == '.mat':  # Matlab :
        from scipy.io import loadmat
        return loadmat(name)
    elif file_ext in ['.npy', '.npz']:  # Numpy (single / multi array)
        import numpy as np
        return np.load(name)
    elif file_ext == '.txt':  # text file
        import numpy as np
        return np.genfromtxt(name)
    elif file_ext == '.json':  # JSON
        return load_json(name)
    elif file_ext in ['.xls', '.xlsx']:  # Excel
        import pandas as pd
        return pd.read_excel(name)
    elif file_ext in ['.xls', '.xlsx']:  # CSV
        import pandas as pd
        return pd.read_csv(name)
    elif file_ext in ['.hdf5', '.h5']:  # HDF5
        import h5py
        return h5py.File(name, 'r')
    else:
        raise IOError("Extension %s not supported." % file_ext)


def safety_save(name):
    """Check if a file name exist.

    If it exist, increment it with '(x)'.
    """
    k = 1
    while os.path.isfile(name):
        fname, fext = os.path.splitext(name)
        if fname.find('(') + 1:
            name = fname[0:fname.find('(') + 1] + str(k) + ')' + fext
        else:
            name = fname + '(' + str(k) + ')' + fext
        k += 1
    return name


def hdf5_write_str(lst):
    """String conversion for writting HDF5.

    Parameters
    ----------
    lst : array_like
        List of strings

    Returns
    -------
    lst : array_like
        Encoded list of strings
    """
    if isinstance(lst, str):
        return lst.encode('ascii', 'ignore')
    else:
        return [k.encode('ascii', 'ignore') for k in lst]


def hdf5_read_str(lst):
    """String conversion for reading HDF5.

    Parameters
    ----------
    lst : array_like
        List of strings

    Returns
    -------
    lst : array_like
        ConveDecodedrted list of strings
    """
    if isinstance(lst, (list, tuple, np.ndarray)):
        return [k.decode('utf-8') for k in lst]
    else:
        return lst.decode('utf-8')
