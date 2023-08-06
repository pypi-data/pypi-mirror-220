import os
import glob
import uuid
import itertools
import numpy as np
import karray as ka
import json
from json import JSONDecodeError
from typing import Union, List, Dict
from .handler import DataCollection
from .settings import settings, allowed_string, value_type_name_map


class SymbolsHandler:
    def __init__(self, method:str, folder_path:str=None, obj:DataCollection=None):
        ''' 
        Initialize SymbolsHandler object.

        Parameters
        ----------
        method : str
            The method used to collect raw variables or symbols. Two methods are available: 1. 'folder' - the symbols are collected from the folder specified by folder_path. 2. 'object' - the variables are collected from the object specified by obj which must be a DataCollection object.
        folder_path : str
            The path to the folder containing the symbols as feather files. Only used if method is 'folder'.
        obj : DataCollection
            The DataCollection object. Only used if method is 'object'.

        Returns
        -------
        None.

        Examples
        --------
        Build symbols from raw scenarios output (parser and loader from arrow tables and feather file format).

            >>> import symbolx as syx
            >>> from symbolx import DataCollection, SymbolsHandler
            >>> DC = DataCollection()
            >>> DC.add_collector(collector_name='opt_model', parser=syx.symbol_parser_feather, loader=syx.load_feather)
            >>> DC.add_folder(collector_name='opt_model', './raw_model_output')
            >>> DC.add_custom_attr(collector_name='opt_model', with_='pandas')
            >>> DC.adquire(id_integer=True, zip_extension=None)
            >>> SH = SymbolsHandler(method='object', obj=DC)

            
        Load symbols from folder.

            >>> from symbolx import , SymbolsHandler
            >>> SH = SymbolsHandler(method='folder', folder_path='./symbols_files')

            
        '''

        assert isinstance(method, str), "Arg 'method' must be a string."
        assert method in ["folder", "object"], "Arg 'method' must be either 'folder' or 'object'"
        self.method = method
        self.folder_path = None
        self.symbols_book = None
        self.symbol_handler_token = str(uuid.uuid4()) # TODO: this can be changed by hashing the input file
        self.saved_symbols = {}
        self.token_info = None
        self.input_method(method=method, folder_path=folder_path, obj=obj)

    def input_method(self, method:str, **kwargs):
        '''
        Input the method used to collect raw variables or symbols.

        Parameters
        ----------
        method : str
            The method used to collect raw variables or symbols. Two methods are available:
            1. 'folder' - the symbols are collected from the folder specified by folder_path.
            2. 'object' - the variables are collected from the object specified by obj which must be a DataCollection object.
        kwargs : dict
            Two keyword arguments are available:
            1. 'folder_path' - the path to the folder containing the symbols as feather files. Only used if method is 'folder'.
            2. 'obj' - the DataCollection object. Only used if method is 'object'.
        
        Returns
        -------
        None.

        '''

        if method == "object":
            self.from_object(obj=kwargs['obj'])
        elif method == "folder":
            self.from_folder(folder_path=kwargs['folder_path'])
        else:
            raise Exception('A method mus be provided from either "object" or "folder"')

    def from_object(self, obj:DataCollection):
        '''
        Extracts information from the DataCollection object, such as variable name and value type. Value type can be either 'value', 'marginal', 'lower', or 'upper' as define in GAMS for variables.

        It also populates a dictionary with the variable name, value type and symbol_handler_token—A symbol_handler_token is generated per instance; this helps to avoid mixup variables of other problems.

        Parameters
        ----------
        obj : DataCollection
            The DataCollection object.

        Returns
        -------
        None.

        '''

        self.symbols_book = obj.symbols_book
        self.collector = obj.collector
        self.short_names = obj.short_names
        for n_v in self.symbols_book:
            settings.append((*n_v,self.symbol_handler_token))


    def from_folder(self, folder_path:str=None):
        '''
        Extracts information from the folder, such as variable name and value type of all symbols saved with extension 'feather'.
        
        Parameters 
        ----------

        folder_path : str
            The path to the folder containing the symbols as feather files. Only used if method is 'folder'.

        Returns
        -------
        None.

        '''

        self.token_info = {}
        self.folder_path = folder_path
        files = glob.glob(os.path.join(self.folder_path, "*.feather"))
        self.symbols_book = {}
        for file in files:
            loaded_file_dict = from_feather_info(file)
            self.symbols_book[(loaded_file_dict['name'],loaded_file_dict['value_type'])] = file

            token = loaded_file_dict['symbol_handler_token']
            settings.append((loaded_file_dict['name'],loaded_file_dict['value_type'],loaded_file_dict['symbol_handler_token']))

            if token not in self.token_info:
                self.token_info[token] = {}
            self.token_info[token][(loaded_file_dict['name'],loaded_file_dict['value_type'])] = file
        if len(self.token_info) > 1:
            print(f"There are Symbols' files with different symbol_handler_token in {folder_path}")
            print("       Symbol's scenario short names or id's might be in conflict.")
            print("       Make sure all Symbols are from the same symbol_handler_token")
            print("       Otherwise, it may happen, for example, different scenarios have the same id.")
            print("       See 'token_info' attribute of SymbolsHandler for more information")


    def append(self, **kwargs):
        '''
        Store a symbol in a temporal container to posterior saving. The container can be accessed by the 'saved_symbols' attribute.

        Parameters
        ----------
        kwargs : dict
            The keyword arguments represents the name of the symbol. value argument is the symbol object.
        
        Returns
        -------
        None.
        
        '''

        for name in kwargs:
            symbol = kwargs[name]
            assert len(set(name).difference(set(allowed_string))) == 0, f"Symbol name '{name}' contains special characters. Please, change the name of the symbol. Allowed chars are: {allowed_string}"
            symbol.name = name
            self.saved_symbols[(name, symbol.value_type)] = symbol

    def save(self, folder_path=None, appended_or_all:str='all', gls:dict=None, overwrite:bool=False):
        '''
        Save the symbols in the temporary container to the folder specified by folder_path.

        Parameters
        ----------
        folder_path : str
            The path of the folder to save the symbols.
        appended_or_all : str
            If appended_or_all is 'all', all symbols contained in gls are saved. If appended_or_all is 'appended', only symbols contained in saved_symbols attribute are saved.
        gls : dictionary
            Recomended globals() that provides a dictionary with all variables from the script or notebook. The current method identifies the variables that are Symbols to be saved.
        overwrite : bool
            If overwrite is True, the symbols present in the folder are overwritten. If overwrite is False, the symbols in the folder are not overwritten. Default is False.

        Returns
        -------
        None.

        '''

        files = glob.glob(os.path.join(folder_path,'*.feather'))
        existing_pairs = {}
        print("Checking folder for duplicate symbol names...")
        for ff in files:
            file = os.path.basename(ff)
            name_sections = file.split('.')
            name = name_sections[0]
            value_type = name_sections[1]
            token = name_sections[2]
            assert (name,value_type) not in existing_pairs, f"Only one symbol name {name}.{value_type} should be found in '{folder_path}' folder. Two or more found\nTokens: {existing_pairs[(name,value_type)]} and {token}"
            existing_pairs[(name,value_type)] = token
        print("Checking passed")
        if folder_path is None:
            assert self.folder_path is not None, "folder_path must be provided"
            folder_path = self.folder_path
        os.makedirs(folder_path, exist_ok=True)
        if appended_or_all == 'all':
            symbol_map = []
            assert gls is not None, "if 'appended_or_all' is 'all' then provide gls=globals() to able to capture all variables that are Symbol instances"
            for name, symbol in gls.items():
                if isinstance(symbol, Symbol):
                    symbol.name = name
                    symbol_map.append(symbol)
        elif appended_or_all == 'appended':
            symbol_map = list(self.saved_symbols.values())
        else:
            raise Exception(f"Function argument 'appended_or_all' must be 'appended' or 'all'. Given: {appended_or_all}")

        for symbol in symbol_map:
            if not overwrite:
                assert (symbol.name,symbol.value_type) not in existing_pairs, f"Only one symbol name {symbol.name}.{symbol.value_type} should be saved in '{folder_path}' folder. Existing file found:\n{symbol.name}.{symbol.value_type}.{existing_pairs[(symbol.name,symbol.value_type)]}.feather"
            file_name = f"{symbol.name}.{symbol.value_type}.{symbol.symbol_handler_token}.feather"
            file_path = os.path.join(folder_path,file_name)
            symbol.to_feather(file_path)

    def get_info(self, symbol_name, value_type):
        '''
        Get information about a symbol.

        Parameters
        ----------
        symbol_name : str
            The name of the symbol.
        value_type : str
            The value type of the symbol.

        Returns
        -------
        symbol_info : dict or str
            if returns a dict, it contains metadata about the symbol and its scenarios. Only works if 'object' was the method used to create the symbol_handler.
            if returns a str, it contains the path to the symbol.feather file. Only works if 'folder' was the method used to create the symbol_handler.

        '''

        assert (symbol_name, value_type) in self.symbols_book, f"Pairs {(symbol_name, value_type)} not present in the symbols_book attribute of SymbolsHandler"
        if isinstance(self.symbols_book[(symbol_name, value_type)], dict):
            return self.symbols_book[(symbol_name, value_type)]
        elif isinstance(self.symbols_book[(symbol_name, value_type)], str):
            return self.symbols_book[(symbol_name, value_type)]

    def __repr__(self):
        return f'''SymbolsHandler(method='{self.method}')'''

def from_feather_dict(path, use_threads=True, with_="polars"):
    '''
    Load a feather file that contains a Symbol and returns a dictionary with symbol array and its metadata.

    Parameters
    ----------
    path : str
        The path to the feather file.
    use_threads : bool
        If True, the feather file is loaded in parallel. If False, the feather file is loaded in serial. Default is True.
    with_ : str
        The name of the python package used to load the arrow table from the feather file. Two options are available: 'polars' or 'pandas'. Default is 'polars'.
    
    Returns
    -------
    symbols_dict : dict
        A dictionary with symbol array and its metadata.

    '''

    import pyarrow.feather as ft
    arr = ka.from_feather(path, use_threads=use_threads, with_=with_)
    restored_table = ft.read_table(path, use_threads=use_threads)
    custom_meta_key = 'symbolx'
    restored_meta_json = restored_table.schema.metadata[custom_meta_key.encode()]
    restored_meta = recurse(restored_meta_json)
    return dict(array=arr,**restored_meta)

def from_feather_info(path):
    '''
    Load a feather file that contains a Symbol and returns a dictionary with symbol name, value type and symbol handler token.

    Parameters
    ----------
    path : str
        The path to the feather file.

    Returns
    -------
    symbols_info : dict
        A dictionary with symbol name, value type and symbol handler token.
    '''

    import pyarrow.feather as ft
    restored_table = ft.read_table(path)
    custom_meta_key = 'symbolx'
    restored_meta_json = restored_table.schema.metadata[custom_meta_key.encode()]
    restored_meta = json.loads(restored_meta_json)
    return dict(name=restored_meta['name'], value_type=restored_meta['value_type'], symbol_handler_token=restored_meta['symbol_handler_token'])

def recurse(d):
    if isinstance(d, dict):
        loaded_d = d
    elif isinstance(d, bytes):
        loaded_d = json.loads(d)
    else:
        return d
    new_dc = {}
    for k, v in loaded_d.items():
        if k.isdigit():
            r = int(k)
        else:
            r = k
        new_dc[r] = recurse(v)
    return new_dc

def build_array(symbol_name:str, value_type:str, symbol_handler:SymbolsHandler):
    """
    Build a symbol array collecting all variable arrays through all scenarios. Only works if 'object' was the method used to create the symbol_handler.
    
    Parameters
    ----------
    symbol_name : str
        The name of the symbol.
    value_type : str
        The value type of the symbol.
    symbol_handler : SymbolsHandler
        The symbol handler.

    Returns
    -------
    symbol_array : karray.Array
        The symbol array.

    """

    list_of_arrays = []
    for scenario_id in symbol_handler.get_info(symbol_name, value_type)['scenario_data']:
        array_with_id = insert_id_dim(symbol_name, value_type, scenario_id, symbol_handler)
        list_of_arrays.append(array_with_id)
    return ka.concat(list_of_arrays)

def insert_id_dim(symbol_name:str, value_type:str, scenario_id:str, symbol_handler:SymbolsHandler):
    """
    Creates an karray.Array from loader function. Then insert to the array a new dimension 'id' with the corresponding scenario_id.

    Parameters
    ----------
    symbol_name : str
        The name of the symbol.
    value_type : str
        The value type of the symbol.
    scenario_id : str
        The id of the scenario.
    symbol_handler : SymbolsHandler
        The symbol handler.

    Returns
    -------
    symbol_array : karray.Array
        The symbol array.

    """

    single_symbol = symbol_handler.get_info(symbol_name, value_type)['scenario_data'][scenario_id]
    single_array_dict = symbol_handler.collector[single_symbol['collector']]['loader'](**single_symbol)
    oarray = ka.Array(**single_array_dict)
    narray = oarray.add_dim(id=symbol_handler.short_names[scenario_id])
    return narray


class Symbol:
    def __init__(
        self,
        name: str=                      None,
        value_type: str=                'v',
        metadata: dict=                 None,
        array: ka.Array=                None,
        symbol_handler_token: str=      None,
        symbol_handler: SymbolsHandler= None,
        ):
        '''
        Symbol constructor.

        Parameters
        ----------
        name : str
            The name of the symbol.
        value_type : str
            The value type of the symbol.
        metadata : dict (optional)
            Nested dictionary with metadata about the symbol. The structure is as follows: {'metadata_1': {1: 'metadata_1_value of scenario 1', 2: 'metadata_2_value of scenario 2'}, ...}
        array : karray.Array
            The symbol array. This must be provided if 'symbol_handler' is not provided.
        symbol_handler_token : str
            The symbol handler token. This must be provided if 'symbol_handler' is not provided.
        symbol_handler : SymbolsHandler
            The symbol handler instance that contains information about the variables and scenarios or the symbol file path.

        Returns
        -------
        symbol : Symbol
            The symbol.

        Examples
        --------
        Based on a symbol_handler

            >>> var1 = Symbol(name='VAR1', symbol_handler=SH)
            >>> var2 = Symbol(name='VAR2', value_type='v', symbol_handler=SH)
            >>> var3 = Symbol(name='VAR3', value_type='m', symbol_handler=SH)

            
        Based on another symbol

            >>> var3_copy = Symbol(name='VAR3_copy', value_type='v', metadata=var3.metadata, array=var3.array, symbol_handler_token=var3.symbol_handler_token)})

            
        Based on a symbol file

            >>> var4 = syx.from_feather(symbol_file_path)

            
        '''
        self.__dict__["_repo"] = {}
        if symbol_handler is not None:
            if 'object' == symbol_handler.method:
                self.build(symbol_handler, name, value_type)
            elif 'folder' == symbol_handler.method:
                self.load(symbol_handler, name, value_type)
        else:
            if settings.exists((name,value_type,symbol_handler_token)):
                print("The symbol name has already been taken by another Symbol stored in SymbolsHandler.")
                print("Please choose another name to avoid overwriting the existing symbol when saving the current symbol.")
            self.name=                 name
            self.value_type=           value_type
            self.metadata=             metadata
            self.array=                array
            self.symbol_handler_token= symbol_handler_token
        self.check_input()
        # optional attributes
        self.dataframe = None


    def __setattr__(self, name, value):
        self._repo[name] = value

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name) # ipython requirement for repr_html
        if name == "dataframe":
            if name in self._repo:
                if self._repo[name] is None:
                    self._repo[name] = self.array.to_pandas()
                    return self._repo[name].copy()
                else:
                    #Sanity check
                    df = self._repo[name]
                    dense = df.value.values.reshape(self.array.shape)
                    if np.allclose(dense, self.array.dense):
                        return df.copy()
                    else:
                        print(f"Getting dataframe again...")
                        self._repo[name] = self.array.to_pandas()
                        return self._repo[name].copy()
            else:
                self.definition_msg(name) # dev msg
        else:
            return self._repo[name]

    def build(self, symbol_handler:SymbolsHandler, name: str=None, value_type: str=None):
        '''
        Populate the symbol instance with information from the symbol handler and the loader function provided to the DataCollection instance.

        Parameters
        ----------
        symbol_handler : SymbolsHandler
            The symbol handler instance that contains information about the variables and scenarios. This method is used when the symbol handler is instantiated with 'object' method.
        name : str
            The name of the symbol.
        value_type : str
            The value type of the symbol.

        Returns
        -------
        symbol : Symbol
            The symbol.

        '''

        assert isinstance(symbol_handler, SymbolsHandler), "'symbol_handler' must be a SymbolsHandler object"
        assert isinstance(name, str), "'name' must be a string"
        assert isinstance(value_type, str), "'value_type' must be a string"
        print(f"{name:<25} value_type: {value_type_name_map[value_type]} ({value_type})")

        key = (name,value_type)
        assert key in symbol_handler.symbols_book, f"'{key}' is not present in 'symbol_handler.symbols_book' dictionary"

        self.name=                 name
        self.value_type=           value_type
        self.metadata=             symbol_handler.get_info(*key)['metadata']
        self.array=                build_array(name, value_type, symbol_handler)
        self.symbol_handler_token= symbol_handler.symbol_handler_token
        
    def load(self, symbol_handler:SymbolsHandler, name: str=None, value_type: str=None):
        '''
        Symbol is recreated from feather file. This method is used when the symbol handler is instantiated with 'folder' method providing the path of the symbol file.

        Parameters
        ----------
        symbol_handler : SymbolsHandler
            The symbol handler instance that contains information about the variables and scenarios. This method is used when the symbol handler is instantiated with 'folder' method.
        name : str
            The name of the symbol.
        value_type : str
            The value type of the symbol.

        Returns
        -------
        symbol : Symbol
            The symbol.

        '''

        assert isinstance(symbol_handler, SymbolsHandler), "'symbol_handler' must be a SymbolsHandler object"
        assert isinstance(name, str), "'name' must be a string"
        assert isinstance(value_type, str), "'value_type' must be a string"
        print(f"{name:<25} value_type: {value_type_name_map[value_type]} ({value_type})")

        key = (name,value_type)
        assert key in symbol_handler.symbols_book, f"'{key}' is not present in 'symbol_handler.symbols_book' dictionary"

        file_path = symbol_handler.get_info(*key)
        symbol_dict = from_feather_dict(file_path, with_=ka.settings.feather_with)
        self.name=                 name
        self.value_type=           value_type
        self.metadata=             symbol_dict['metadata']
        self.array=                symbol_dict['array']
        self.symbol_handler_token= symbol_dict['symbol_handler_token']

    def to_arrow(self):
        '''
        Convert the symbol to an arrow table with metadata. The symbol array contains karray array and the karray metadata. The returned table contains karray and symbox metadata as well.

        Returns
        -------
        arrow_table : pyarrow.Table
            The arrow table.

        '''

        table = self.array.to_arrow()
        existing_meta = table.schema.metadata
        custom_meta_key = 'symbolx'
        custom_metadata = {}
        attr = ['name', 'value_type', 'metadata','symbol_handler_token']
        for k,v in self._repo.items():
            if k in attr:
                custom_metadata[k] = v

        custom_meta_json = json.dumps(custom_metadata)
        existing_meta = table.schema.metadata
        combined_meta = {custom_meta_key.encode() : custom_meta_json.encode(),**existing_meta}
        table = table.replace_schema_metadata(combined_meta)
        return table

    def to_feather(self, path:str):
        '''
        Convert the symbol to a feather file with metadata. The symbol array contains karray array and the karray metadata. The returned table contains karray and symbox metadata as well.

        Parameters
        ----------
        path : str
            The path of the feather file.

        Returns
        -------
        None

        '''

        import pyarrow.feather as ft
        sets = set(allowed_string)
        sets.add(os.path.sep)
        joint = ''.join(sorted(sets))
        assert len(set(path).difference(sets)) == 0, f"There are/is special characters in path '{path}'. Allowed chars are: {joint}"

        table = self.to_arrow()
        ft.write_feather(table, path)
        print(f"{path}")
        return None

    def check_input(self):
        '''
        Check the input of the symbol. 

        Returns
        -------
        None

        '''

        assert self.name is not None and isinstance(self.name, str), "Name of symbol must be provided."
        assert self.value_type is not None and isinstance(self.value_type, str), "Value type of symbol must be provided."
        assert self.metadata is not None and isinstance(self.metadata, dict), "metadata of symbol must be provided."
        assert self.array is not None and isinstance(self.array, ka.Array), "Array must be provided."
        assert self.symbol_handler_token is not None and isinstance(self.symbol_handler_token, str), "Symbol handler token must be provided."

    @property
    def dims(self):
        '''
        Get the dimensions of the symbol.

        Returns
        -------
        dims : list of strings
            The dimensions of the symbol.

        '''
        return self.array.dims

    @property
    def df(self):
        '''
        Get the dataframe of the symbol with the dimenssions coordinates as multiindex. It contains all possible combinations of the dimensions coordinates.

        Returns
        -------
        df : pandas.DataFrame
            The multiindex dataframe of the symbol. Long data format.

        '''

        return self.dataframe.set_index(self.array.dims)

    @property
    def dfm(self):
        '''
        Get the dataframe of the symbol with metadata as additional columns. Dimenssions coordinates are as columns.

        Returns
        -------
        dfm : pandas.DataFrame
            The dataframe of the symbol with long data format.

        '''

        dfm = self.dataframe
        for k, v in self.metadata.items():
            dfm[k] = dfm["id"].map(v)
        return dfm

    @property
    def dfc(self):
        '''
        Get the dataframe of the symbol with only custom metadata as additional columns. Dimenssions coordinates are as columns.

        Returns
        -------
        dfc : pandas.DataFrame
            The dataframe of the symbol with long data format.

        '''

        dfc = self.dataframe
        for k, v in self.metadata.items():
            if 'custom_' in k:
                dfc[k] = dfc["id"].map(v)
        return dfc
    
    def to_polars(self):
        '''
        Convert the symbol to a polar data frame.

        Returns
        -------
        polar_df : polars.DataFrame
            The polar data frame of the symbol.

        '''

        return self.array.to_polars()

    def to_pandas(self):
        '''
        Convert the symbol to a pandas data frame.

        Returns
        -------
        pandas_df : pandas.DataFrame
            The pandas data frame of the symbol.

        '''

        return self.array.to_pandas()

    def metadata_union(self, other=None):
        '''
        Union the metadata of two symbols.

        Parameters
        ----------
        other : Symbol

        Returns
        -------
        metadata : dict
            The union of the metadata of two symbols.

        '''

        self_metadata = self.metadata
        other_metadata = other.metadata
        new_metadata = {}
        for elem in self_metadata.keys():
            new_metadata[elem] = {**self_metadata[elem],**other_metadata[elem]}
        return new_metadata

    def new_symbol(self, array, new_name, other=None):
        '''
        Create a new symbol with a new name and a new array.

        Parameters
        ----------
        array : ka.Array
            The array of the new symbol.
        new_name : str
            The name of the new symbol.
        other : Symbol
            The other symbol.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        if isinstance(other, Symbol):
            assert self.symbol_handler_token == other.symbol_handler_token, "Symbol handler tokens must be the same"
            new_metadata = self.metadata_union(other)
        elif other is None or isinstance(other,(int,float)):
            new_metadata = self.metadata
        else:
            raise Exception(f'other must be either a Symbol object, int, float or None, but it is: {str(type(other))}')
        new_object = Symbol(name=new_name, value_type='v',
                            metadata=new_metadata, array=array, 
                            symbol_handler_token=self.symbol_handler_token)
        return new_object

    def __add__(self, other):
        '''
        Add two symbols or a symbol and an number.

        Parameters
        ----------
        other : Symbol or int or float
            The symbol or number to add.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        if isinstance(other, (int, float)):
            new_array = self.array + other
            new_name =  f"({self.name})+{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, Symbol):
            new_array = self.array + other.array
            new_name = f"({self.name})+({other.name})"
            return self.new_symbol(new_array, new_name, other)
        else:
            raise Exception(f'{type(other)} is not supported')

    def __sub__(self, other):
        '''
        Subtract two symbols or a symbol and an number.

        Parameters
        ----------
        other : Symbol or int or float
            The symbol or number to subtract.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        if isinstance(other, (int, float)):
            new_array = self.array - other
            new_name =  f"({self.name})-{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, Symbol):
            new_array = self.array - other.array
            new_name = f"({self.name})-({other.name})"
            return self.new_symbol(new_array, new_name, other)
        else:
            raise Exception(f'{type(other)} is not supported')

    def __mul__(self, other):
        '''
        Multiply two symbols or a symbol and an number.

        Parameters
        ----------
        other : Symbol or int or float
            The symbol or number to multiply.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Exceptions
        ----------
        Exception 1 : if the two symbols have no common dimensions.
        Exception 2 : if the two symbols have more than one uncommon dimensions.
        Exception 3 : if the class of other is not a Symbol or int or float.

        '''

        if isinstance(other, (int, float)):
            new_array = self.array * other
            new_name = f"({self.name})*{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, Symbol):
            diffdims = list(set(self.dims).symmetric_difference(other.dims))
            lendiff = len(diffdims)
            if set(self.dims) == set(other.dims):
                new_array = self.array * other.array
                new_name = f"({self.name})*({other.name})"
                return self.new_symbol(new_array, new_name, other)
            elif lendiff == 1:
                new_array = self.array * other.array
                new_name = f"({self.name})*({other.name})"
                return self.new_symbol(new_array, new_name, other)
            elif lendiff > 1:
                common_dims = list(set(self.dims).intersection(other.dims))
                if len(common_dims) > 0:
                    new_array = self.array * other.array
                    new_name = f"({self.name})*({other.name})"
                    return self.new_symbol(new_array, new_name, other)
                else:
                    raise Exception(f"The difference in dimensions is greater than one: '{diffdims}' and has no common dimensions")
        else:
            raise Exception(f'{type(other)} is not supported')

    def __truediv__(self, other):
        '''
        Divide two symbols or a symbol and an number.
        
        Parameters
        ----------
        other : Symbol or int or float
            The symbol or number to divide.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Exceptions
        ----------
        Exception 1 : if the difference in dimensions is greater than one.
        Exception 2 : if the class of other is not a Symbol or int or float.

        '''

        if isinstance(other, (int, float)):
            new_array = self.array / other
            new_name = f"({self.name})/{str(other)}"
            return self.new_symbol(new_array, new_name, other)
        elif isinstance(other, object):
            diffdims = set(self.dims).symmetric_difference(other.dims)
            lendiff = len(diffdims)
            if set(self.dims) == set(other.dims):
                new_array = self.array / other.array
                new_name = f"({self.name})/({other.name})"
                return self.new_symbol(new_array, new_name, other)
            elif lendiff == 1:
                new_array = self.array / other.array
                new_name = f"({self.name})/({other.name})"
                return self.new_symbol(new_array, new_name, other)

            elif lendiff > 1:
                raise Exception(f"The difference in dimensions is greater than one: '{diffdims}'")
        else:
            raise Exception("The second term is not known, must be a int, float or a Symbol object")

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            new_array =  other + self.array
            new_name = f"{str(other)}+({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            new_array = other - self.array
            new_name = f"{str(other)}-({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            new_array = other*self.array
            new_name = f"{str(other)}*({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            new_array = other/self.array
            new_name = f"{str(other)}/({self.name})"
            return self.new_symbol(new_array, new_name, other)

    def rename(self, new_name: str):
        '''
        Rename the symbol.

        Parameters
        ----------
        new_name : str
            The new name of the symbol.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        return self.new_symbol(self.array, new_name)

    def dimreduc(self, dim:str='h', aggfunc=np.add.reduce):
        '''
        Reduce one dimension of the symbol by applying a numpy ufunc over all coordinates of the dimension.
        
        Parameters
        ----------
        dim : str
            The dimension to reduce.
        aggfunc : ufunc
            The numpy ufunc to apply. Options are [np.add.reduce,np.multiply.reduce,np.average]. Default np.add.reduce

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.reduce(dim, aggfunc)
        new_name = f"({self.name}).dimreduc({dim},{aggfunc})"
        return self.new_symbol(new_array, new_name)

    @property
    def items(self):
        '''
        Get the items of the symbol or coordinates.

        Returns
        -------
        coords: dict
            The items of the symbol or coordinates.

        '''

        return self.array.coords

    def rename_dim(self, **kwargs):
        """ 
        Rename a dimension of the symbol.

        Parameters
        ----------
        kwargs : dict
            The keyword arguments can be the current dimensions name and the value arguments are the new name of the dimensions.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        """

        new_array = self.array.rename(**kwargs)
        new_name = f"({self.name}).rename_dim(**{kwargs})"
        return self.new_symbol(new_array, new_name)
    
    def add_dim(self, dim_name: str, value: Union[str,int,dict]):
        '''
        Deprecated: Use add_dims instead.

        Add a dimension to the symbol.

        Parameters
        ----------
        dim_name : str
            The name of the dimension.
        value : Union[str,int,dict]
            if value is a string, the dimension column will contain this value only. if value is a dict, the dict must look like {column_header:{column_element: new_element_name}} where column_header must currently exists and all column_elements must have a new_element_name.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        if isinstance(value, (str,int)):
            new_array = self.array.add_dim(**{dim_name:value})
            new_name = f"({self.name}).add_dim({dim_name},{value})"
            return self.new_symbol(new_array, new_name)

        elif isinstance(value, dict):
            new_array = self.array.add_dim(**{dim_name:value})
            new_name = f"({self.name}).add_dim({dim_name},{value})"
            return self.new_symbol(new_array, new_name)
        else:
            raise Exception('value is neither str nor dict')
        
    def add_dims(self, **kwargs):
        '''
        Add a dimension to the symbol.

        Parameters
        ----------
        kwargs : dict
            The keyword arguments must be new dimension names and the value arguments contain information of the new coordinates as folows:
            value arguments : Union[str, int, dict[str, dict[str,str]], dict[str,list]]
            if value is a string or integer, the new dimension will contain this value only as a unique coordinate.
            if value is a dict of dict, the dict must look like {existing dimension mane:{current coordinate: new coordinate}}
            if value is a dict of list, the dict must look like {existing dimension mane:[numpy array of current coordinate, numpy array of new coordinate]} both arrays must have the same length. Numpy array of current coordinate must be unique. The position of the elements of the arrays is considered for the replacement.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.add_dim(**kwargs)
        new_name = f"({self.name}).add_dims({','.join(list(kwargs))})"
        return self.new_symbol(new_array, new_name)

    def dropna(self):
        '''
        Drop the NaN values from the symbol.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.dropna()
        new_name = f"({self.name}).dropna()"
        return self.new_symbol(new_array, new_name)

    def dropinf(self, pos:bool, neg:bool):
        '''
        Drop the inf values from the symbol.
        
        Parameters
        ----------
        pos : bool
            If True, drop the inf values from the positive direction.
        neg : bool
            If True, drop the inf values from the negative direction.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.dropinf(pos,neg)
        new_name = f"({self.name}).dropna({pos=},{neg=})"
        return self.new_symbol(new_array, new_name)

    def drop(self, dims:Union[str,List[str]]):
        '''
        Drop the specified dimensions from the symbol.

        Parameters
        ----------
        dims : Union[str,List[str]]
            The dimensions to drop.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.drop(dims=dims)
        new_name = f"({self.name}).dropna({dims=})"
        return self.new_symbol(new_array, new_name)

    def round(self, decimals:int):
        '''
        Round the symbol to the specified number of decimals.

        Parameters
        ----------
        decimals : int
            The number of decimals to round to.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.round(decimals=decimals)
        new_name = f"({self.name}).round({decimals=})"
        return self.new_symbol(new_array, new_name)

    def elems_to_datetime(self, new_dim:str, actual_dim:str, reference_date:str='01-01-2030', freq:str='H', sort_corrds:bool=True):
        '''
        Convert the elements of the symbol to datetime.

        Parameters
        ----------
        new_dim : str
            The new dimension name.
        actual_dim : str
            The actual dimension name.
        reference_date : str
            The reference date.
        freq : str
            The frequency of the datetime.
        sort_corrds : bool
            If True, sort the coordinates of the symbol.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.elems_to_datetime(new_dim=new_dim, actual_dim=actual_dim, reference_date=reference_date, freq=freq, sort_coords=sort_corrds)
        new_name = f"({self.name}).elems_to_datetime({new_dim}{actual_dim},{reference_date},{freq},{sort_corrds})"
        return self.new_symbol(new_array, new_name)

    def elems_to_int(self, new_dim:str, actual_dim:str):
        '''
        Convert the elements of the symbol to integers.

        Parameters
        ----------
        new_dim : str
            The new dimension name.
        actual_dim : str
            The actual dimension name.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        '''

        new_array = self.array.elems_to_int(new_dim, actual_dim)
        new_name = f"({self.name}).elems_to_int({new_dim=},{actual_dim=})"
        return self.new_symbol(new_array, new_name)

    def find_ids(self, **kwargs):
        '''
        Find scenarios ids in a symbol that comply with the criteria given by the keyword arguments. Several criteria can be specified where the result would be the intersection of all criteria.

        Parameters
        ----------
        kwargs : dict
            The keyword arguments must be the following:

            metadata name : str
                Metadata feature name.
            criteria : Tuple[str,Union[str,int,float]]
                The criteria to match. It is a tuple of two elements. The first element is a string that represents an operator such as '>', '<', '<=', '>=', '==', or '!='. The second element is the value to match.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Examples
        --------
        >>> Z.find_ids(**{'time_series_scen':('==','NaN'),'co2price(n,tech)':('<',80)})

        '''

        dc = self.metadata
        collector = []
        for k,v in dc.items():
            if k in kwargs.keys():
                flag = False
                nan_str = False
                id_list = []
                for k2, v2 in v.items():
                    if isinstance(v2,str):
                        if isinstance(kwargs[k][1],str):
                            if eval(f"'{v2}' {kwargs[k][0]} '{kwargs[k][1]}'"):
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                            if kwargs[k][1] != 'NaN' and v2 == 'NaN':
                                nan_str = True
                        else:
                            continue
                    elif np.isnan(v2):
                        if np.isnan(kwargs[k][1]):
                            if kwargs[k][0] == '==':
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                        else:
                            if kwargs[k][0] == '!=':
                                id_list.append(k2)
                                if not flag:
                                    flag = True
                            elif kwargs[k][0] != '==':
                                print(f"{k} in {k2} has NaN value for condition '{kwargs[k][0]} {str(kwargs[k][1])}'. Not included")
                            
                    elif np.isnan(kwargs[k][1]):
                        if kwargs[k][0] == '!=':
                            id_list.append(k2)
                            if not flag:
                                flag = True
                        else:
                            continue
                    elif eval(f"{v2} {kwargs[k][0]} {kwargs[k][1]}"):
                        id_list.append(k2)
                        if not flag:
                            flag = True
                collector.append(set(id_list))
                if not flag:
                    print(f"Column '{k}' does not contain '{kwargs[k][1]}'")
                if nan_str:
                    print(f"Column '{k}' has 'NaN' as string. You can filter such string too.")
        not_present = []
        for cond in kwargs.keys():
            if cond in dc.keys():
                pass
            else:
                not_present.append(cond)
        if not_present:
            str_cond = ";".join(not_present)
            print(f"{str_cond} not in symbol's data")
        return set.intersection(*collector)

    def id_info(self, ID:Union[str,int]):
        '''
        Get information about a scenario id.

        Parameters
        ----------
        ID : Union[str,int]
            The scenario id.

        Returns
        -------
        dc : dict
            A dictionary with the following  as keys and the corresponding value.

        Examples
        --------

           >>> Z.id_info('S0001')

        '''

        dc = dict()
        for k, v in self.metadata.items():
            if ID in v.keys():
                dc[k] = v[ID]
        return dc
    
    def shrink(self, neg: Union[bool, list]=False, **kwargs):
        ''' 
        Shrinks the symbol to keep only those coordinates that comply the given criteria.
        karg is a dictionary of symbol sets as key and elements of the set as value.
        sets and elements must be present in the symbol.

        Parameters
        ----------
        neg : Union[bool, List[bool]]
            If True, the symbol is shrunk to keep only those coordinates that do not comply the criteria. If False, the symbol is shrunk to keep only those coordinates that comply the criteria.
            If a list of booleans, follows the same order as the dimensions provided as kwargs.
            Defaut is False.
        kwargs : dict
            The keyword arguments must be the following:

            dimension name : str (dictionary keys)
                dimesion name with the coordinates to keep if neg is False.
            coordinates list: list (dictionary values)
                    list of coordinates to keep if neg is True.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Examples
        --------
        >>> Z.shrink(neg=[False, True], **{'tech':['pv','bio'],'h':[1,2]})

        >>> Z.shrink(neg=[False, True], tech=['pv','bio'], h=[1,2])

        '''

        if len(kwargs) > 1:
            if isinstance(neg,list):
                assert len(neg) == len(kwargs)
            else:
                new_neg = []
                for _ in range(len(kwargs)):
                    new_neg.append(neg)
                neg = new_neg
        else:
            neg = [neg]

        for key, value in kwargs.items():
            if key in self.dims:
                if set(value).issubset(self.items[key]):
                    pass
                else:
                    not_present = set(value) - (set(value) & set(self.items[key]))
                    present = (set(value) & set(self.items[key]))
                    if len(present) == 0:
                        raise Exception(f"{not_present} is/are not in {self.items[key]}")
                    else:
                        # print(f"    Only {present} exist in {self.items[key]} and meet criteria at '{key}', while not {not_present}")
                        kwargs[key] = sorted(present)
            else:
                raise Exception(f"'{key}' is not in {self.dims} for symbol {self.name}")

        right_kwargs = {k:v for k,v in kwargs.items()}
        i = 0
        for key in kwargs:
            if neg[i]:
                all_elems = self.items[key].tolist()
                for skip_elem in kwargs[key]:
                    all_elems.remove(skip_elem)
                right_kwargs[key] = all_elems

        new_array = self.array.shrink(**right_kwargs)
        new_name = f"({self.name}).shrink(neg={neg},{','.join(['='.join([k,str(v)]) for k,v in kwargs.items()])})"
        return self.new_symbol(new_array, new_name)

    def shrink_by_attr(self, neg=False, **kwargs):
        ''' 
        shrink_by_attributes generates new symbol based on metadata attributes of the symbol. Attributes can be seen with symbol_object.metadata.
        Shrink the symbol to keep only the coordinates that comply with the criteria given in kwargs.

        Parameters
        ----------
        neg : bool
            If True, the symbol is shrunk to keep only those ids that do not comply the criteria. If False, the symbol is shrunk to keep only those ids that comply the criteria.
            Defaut is False.
        kwargs : dict
            The keyword arguments must be the following:

            metadata name : str (dictionary keys)
                metadata name to consider as criteria.
            metadata elements : str (dictionary values)
                    metadata elements to keep if neg is False. If neg is True, the metadata elements that do not comply the criteria are kept.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Examples
        --------
        >>> Z.shrink_by_attr(**{'run':[0,1], 'country_set':['NA']})

        >>> Z.shrink_by_attr(run=[0,1], country_set=['NA'])

        '''
        for key, value in kwargs.items():
            dc = self.metadata
            if key not in dc.keys():
                raise Exception(f"'{key}' is not in {list(dc.keys())} for symbol {self.name}")
        
        id_list = sorted(set([item for sublist in list(self.create_mix(kwargs).values()) for item in sublist]))
        new_object = self.shrink(id=id_list, neg=neg)
        new_object.name = f"(neg={neg},{self.name}).shrink_by_attr({','.join(['='.join([k,str(v)]) for k,v in kwargs.items()])})"
        return new_object

    def refdiff(self, reference_id:Union[int,str]=0):
        ''' 
        Returns the difference between the reference scenario (with its respective id) and the rest of the scenarios in a symbol. The symbol must have the dimension name 'id'.
        
        Parameters
        ----------
        reference_id : Union[int,str]
            The id of the reference scenario.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Examples
        --------

        >>> Z.refdiff(reference_id='S0001')
        
        '''
        new_object = self - self.shrink(id=[reference_id]).dimreduc('id')
        new_object.name = f"({self.name}).refdiff({reference_id})"
        return new_object

    def create_mix(self, criteria):
        ''' 
        Private function used for refdiff_by_sections.
        '''

        combination = self.create_combination(criteria)
        order = criteria.keys()
        return self._find_ids_by_tuple(order,combination)

    def create_combination(self, criteria: dict):
        '''
        Private function used for refdiff_by_sections.
        '''

        return list(itertools.product(*criteria.values()))


    def _find_ids_by_tuple(self,key_order,combination):
        '''
        Private function used for refdiff_by_sections.
        '''

        groups = {}
        for i, pair in enumerate(combination):
            config = {}
            for k, v in zip(key_order, pair):
                config[k] = ('==',v)
            groups[i] = list(self.find_ids(**config))
        return groups

    def _ref_diff_group(self,refs,groups, verbose=False):
        '''
        Private function used for refdiff_by_sections.
        '''

        symbols = []
        for key in groups:
            if len(refs[key]) == 0:
                if verbose:
                    print(f"{refs} for key = {key} no reference id found")
                    print(groups)
                continue
            else:
                refdiff_symbol = self.shrink(id=list(groups[key])).refdiff(refs[key][0])
                symbols.append(refdiff_symbol)
        return sum(symbols)

    def refdiff_by_sections(self, criteria_dict, criteria_ref_dict, verbose=False):
        '''
        Returns the difference between the reference scenario following criteria based on the metadata attributes. 

        Parameters
        ----------
        criteria_dict : dict
            The criteria dictionary contains the metadata attributes as keys and the criteria as values.
        criteria_ref_dict : dict
            The reference criteria dictionary.
        verbose : bool
            If True, prints the results. Defaut is False.

        Returns
        -------
        new_symbol : Symbol
            The new symbol.

        Examples
        --------
        
        >>> Z.refdiff_by_sections(**{'run':[0,1], 'country_set':['NA']})

        '''

        groups = self.create_mix(criteria_dict)
        criteria_ref_full = {**criteria_dict,**criteria_ref_dict}
        refs = self.create_mix(criteria_ref_full)
        assert all([len(refs[key]) <= 1 for key in refs]), f"It should be only one reference scenario per group {criteria_ref_full.keys()} but more were found: {refs}"
        return self._ref_diff_group(refs,groups,verbose)

    def definition_msg(self, name):
        print(f"Attribute '{name}' must be defined first in __init__ method")

    def __repr__(self):
        return f'''Symbol(name='{self.name}', \n       value_type='{self.value_type}')'''


def from_feather(path):
    return Symbol(**from_feather_dict(path, with_=ka.settings.feather_with))