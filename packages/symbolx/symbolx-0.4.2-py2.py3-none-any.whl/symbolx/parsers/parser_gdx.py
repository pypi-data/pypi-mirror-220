import os
import zipfile
import tempfile
import numpy as np
import platform
import subprocess
from ..utils import _get_files_path_list, _convert_symbol_name_to_tuple


def symbol_parser_gdx(folder: str, symbol_names: list=[], zip_extension=None, **kwargs):
    '''
    Parse all symbols from a folder and returns a dictionary
    '''
    gams_dir = kwargs['gams_dir'] if 'gams_dir' in kwargs else None
    ret, gams_dir = get_gams_dir(gams_dir=gams_dir)
    if not ret:
        raise Exception("Gams directory not found")

    symbol_dict_with_value_type = {}
    for symbs in symbol_names:
        symb_tp = _convert_symbol_name_to_tuple(symbs)
        symbol_dict_with_value_type[symb_tp] = None

    file_list = _get_files_path_list(folder=folder, zip_extension=zip_extension, file_extension='gdx')

    symbol_list = []
    for file in file_list:
        scen_id = os.path.basename(file).split('.')[0]
        if zip_extension is not None:
            path_parts = file.split(zip_extension+os.sep)
            zip_fpath = path_parts[0] + zip_extension
            target_fpath = path_parts[1]
            with zipfile.ZipFile(zip_fpath, mode="r") as zip_io:
                listOfFileNames = zip_io.namelist()
                assert target_fpath in listOfFileNames
                with tempfile.TemporaryDirectory() as tmpdirname:
                    zip_io.extract(target_fpath, tmpdirname)
                    tempfile_path = os.path.join(tmpdirname,target_fpath)
                    symbol_items = _symbols_list_from_gdx(tempfile_path, gams_dir)
        else:
            symbol_items = _symbols_list_from_gdx(file, gams_dir)

        for (name, symb_type, nrdims) in symbol_items:
            if symb_type == 0: # set
                options = []
            elif symb_type == 1: # parameter
                options = ['v']
            elif symb_type == 2: # variable
                options = ['v', 'm']
            elif symb_type == 3: # equation
                options = ['v', 'm']
            for value_type in options:
                symb_tp = (name, value_type)
                if symb_tp in symbol_dict_with_value_type or len(symbol_names) == 0:
                                        # This fields are mandatory for a parser
                    symbol_list.append({'symbol_name':symb_tp[0],
                                        'value_type':symb_tp[1],
                                        'path':file,
                                        'scenario_name':scen_id,
                                        # Until here
                                        # you can add more (custom) attributes. It must be added also see handler.py def add_custom_attr() and be an attribute for loader
                                        'gams_dir':gams_dir,
                                        'zip_extension':zip_extension,
                                        'inf_to_zero':True, # included with default value. This can be changed later in handler.py def add_custom_attr()
                                        'verbose':False,
                                        })
    return symbol_list

def load_gdx(symbol_name: str, value_type: str='v', path: str='', gams_dir: str= None, inf_to_zero:bool=True, verbose:bool=False, zip_extension=None, **kwargs):
    '''
    Load custom GDX file.

    Parameters
    ----------
    symbol_name : str
        Name of the symbol to be extracted.
    value_type : str, optional
        Type of the symbol to be extracted. The default is 'v'.
    path : str
        Path to the gdx file.
    gams_dir : str, optional

    '''
    value_types = {'v':0, 'm':1, 'lo':2, 'up':3, 'scale':4}
    assert value_type in value_types.keys(), f'value_type must be one of the following: {value_types.keys()}'
    if zip_extension is not None:
        path_parts = path.split(zip_extension+os.sep)
        zip_fpath = path_parts[0] + zip_extension
        target_fpath = path_parts[1]
        with zipfile.ZipFile(zip_fpath, mode="r") as zip_io:
            listOfFileNames = zip_io.namelist()
            assert target_fpath in listOfFileNames
            with tempfile.TemporaryDirectory() as tmpdirname:
                zip_io.extract(target_fpath, tmpdirname)
                tempfile_path = os.path.join(tmpdirname,target_fpath)
                metadata = _gdx_get_symbol_data_dict(symbol_name=symbol_name, gdx_file=tempfile_path, gams_dir=gams_dir)
                symbol = _gdx_get_symbol_array_str(symbol_name=symbol_name, gdx_file=tempfile_path, gams_dir=gams_dir)
                nrdims = len(metadata['dims'])
                col_index = nrdims + value_types[value_type]
                raw_coo = symbol[:, list(range(nrdims)) + [col_index]]
                # Warning: gams2numpy pkg convert EPS to INF as 5e+300
                if inf_to_zero:
                    EPS = raw_coo[:, nrdims] == np.float64("5e+300")
                    raw_coo[EPS, nrdims] = 0.0
                    if verbose:
                        if sum(EPS) > 0:
                            print('GAMS EPS to 0.0 changed')
                value = raw_coo[:, nrdims].astype(float)
                index = {dim: raw_coo[:,idx] for idx, dim in enumerate(metadata['dims'])}
                coords = {dim: metadata['coords'][dim] for dim in metadata['dims']}
                return {'data': (index, value),'coords': coords}
    else:
        metadata = _gdx_get_symbol_data_dict(symbol_name=symbol_name, gdx_file=path, gams_dir=gams_dir)
        symbol = _gdx_get_symbol_array_str(symbol_name=symbol_name, gdx_file=path, gams_dir=gams_dir)
        nrdims = len(metadata['dims'])
        col_index = nrdims + value_types[value_type]
        raw_coo = symbol[:, list(range(nrdims)) + [col_index]]
        # Warning: gams2numpy pkg convert EPS to INF as 5e+300
        if inf_to_zero:
            EPS = raw_coo[:, nrdims] == np.float64("5e+300")
            raw_coo[EPS, nrdims] = 0.0
            if verbose:
                if sum(EPS) > 0:
                    print('GAMS EPS to 0.0 changed')
        value = raw_coo[:, nrdims].astype(float)
        index = {dim: raw_coo[:,idx] for idx, dim in enumerate(metadata['dims'])}
        coords = {dim: metadata['coords'][dim] for dim in metadata['dims']}
        return {'data': (index, value),'coords': coords}

def _symbols_list_from_gdx(filename: str = None, gams_dir: str = None):
    """ It returns a list of symbols' names contained in the GDX file

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed

    Returns:
        list: a list of symbol's names contained in the GDX file
    """
    try:
        from gdxcc import (
            gdxSystemInfo,
            gdxSymbolInfo,
            gdxCreateD,
            gdxOpenRead,
            gdxDataReadDone,
            new_gdxHandle_tp,
            gdxClose,
            gdxFree,
            GMS_SSSIZE,
        )
    except:
        from gams.core.gdx import (
            gdxSystemInfo,
            gdxSymbolInfo,
            gdxCreateD,
            gdxOpenRead,
            gdxDataReadDone,
            new_gdxHandle_tp,
            gdxClose,
            gdxFree,
            GMS_SSSIZE,
        )

    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    gdxOpenRead(gdxHandle, filename)
    exists, nSymb, nElem = gdxSystemInfo(gdxHandle)
    symbols = []
    for symNr in range(nSymb):
        ret, name, nrdims, symb_type = gdxSymbolInfo(gdxHandle, symNr)
        symbols.append((name, symb_type, nrdims))
    gdxDataReadDone(gdxHandle)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return symbols

def _gdx_get_symbol_array_str(symbol_name: str, gdx_file: str,  gams_dir: str=None):
    try:
        from gams2numpy import Gams2Numpy
    except:
        from gams.numpy import Gams2Numpy

    g2np = Gams2Numpy(gams_dir)
    uel_map = g2np.gdxGetUelList(gdx_file)
    arr = g2np.gdxReadSymbolStr(gdx_file, symbol_name,uel_map)
    return arr

def _gdx_get_symbol_data_dict(symbol_name: str, gdx_file: str, gams_dir: str=None):

    try:
        from gdxcc import (
            gdxSymbolInfo,
            gdxFindSymbol,
            gdxSymbolGetDomainX,
            gdxSymbolInfoX,
            gdxCreateD,
            gdxOpenRead,
            new_gdxHandle_tp,
            gdxClose,
            gdxFree,
            GMS_SSSIZE,
        )
    except:
        from gams.core.gdx import (
            gdxSymbolInfo,
            gdxFindSymbol,
            gdxSymbolGetDomainX,
            gdxSymbolInfoX,
            gdxCreateD,
            gdxOpenRead,
            new_gdxHandle_tp,
            gdxClose,
            gdxFree,
            GMS_SSSIZE,
        )

    gdxHandle = new_gdxHandle_tp()
    ret, msg = gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    ret, msg = gdxOpenRead(gdxHandle, gdx_file)
    assert ret, f"Failed to open '{gdx_file}'"
    ret, symidx = gdxFindSymbol(gdxHandle, symbol_name)
    assert ret, f"Symbol {symbol_name} not found in {gdx_file}"
    if not ret:
        return None
    _, name, NrDims, data_type = gdxSymbolInfo(gdxHandle, symidx)
    _, gdx_domain = gdxSymbolGetDomainX(gdxHandle, symidx)
    _, NrRecs, _, description = gdxSymbolInfoX(gdxHandle, symidx)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)

    data = {}
    data['symbol'] = symbol_name
    data['dims'] = gdx_domain
    data['coords'] = {dim: sorted(np.sort(_gdx_get_symbol_array_str(symbol_name=dim, gdx_file=gdx_file, gams_dir=gams_dir)[:,0])) for dim in gdx_domain}
    return data



def find_gams():
    if platform.system() == "Linux":
        path = subprocess.check_output(['which', 'gams']).decode().rstrip('\n')
        if path:
            gams_dir_path = os.path.dirname(path)
            exists = os.path.exists(gams_dir_path)
            return exists, gams_dir_path
    elif platform.system() == "Windows":
        path = subprocess.check_output(["where", "gams"]).decode().rstrip('\n')
        if path:
            gams_dir_path = os.path.dirname(path)
            exists = os.path.exists(gams_dir_path)
            return exists, gams_dir_path
    elif platform.system() == "Darwin":
        path = subprocess.check_output(['which', 'gams']).decode().rstrip('\n')
        if path:
            gams_dir_path = os.path.dirname(path)
            exists = os.path.exists(gams_dir_path)
            return exists, gams_dir_path
    return False, None

def exists_gams(gams_dir):
    if gams_dir is None:
        return False, None
    else:
        if os.path.exists(gams_dir):
            path = os.path.join(gams_dir, 'gams')
            try:
                script = subprocess.check_output([path]).decode().rstrip('\n')
                return True, gams_dir
            except FileNotFoundError:
                return False, gams_dir
        else:
            return False, gams_dir
        
def get_gams_dir(gams_dir):
    if gams_dir is None:
        ret, gams_dir = find_gams()
        if ret:
            print(f"Found gams in {gams_dir}")
            return ret, gams_dir
        else:
            print(f'''
                  gams cannot be detected. Make sure you have gams installed. 
                  If gams is already installed, add gams_dir argument with the correct path to gams 
                  e.g. data_collection_instance.adquire(gams_dir="gams/path/here"); or
                  add gams directory to the PATH.
                  ''')
            return ret, gams_dir
    else:
        ret, gams_dir = exists_gams(gams_dir)
        if ret:
            return ret, gams_dir
        else:
            old_gams_dir = gams_dir
            ret, gams_dir = find_gams()
            if ret:
                print(f"Given gams_dir '{old_gams_dir}' was not found. Trying gams in {gams_dir}")
                return ret, gams_dir
            else:
                print(f'''
                    gams was not found in the provided gams_dir {gams_dir}. 
                    Make sure you have gams installed. 
                    If gams is already installed, add gams_dir argument with the correct path to gams 
                    e.g. data_collection_instance.adquire(gams_dir="gams/path/here"); or
                    add gams directory to the PATH.
                    ''')
                return ret, gams_dir

