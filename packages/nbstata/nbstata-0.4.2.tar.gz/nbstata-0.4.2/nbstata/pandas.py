# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/06_pandas.ipynb.

# %% auto 0
__all__ = ['better_dataframe_from_stata', 'better_pdataframe_from_data', 'better_pdataframe_from_frame']

# %% ../nbs/06_pandas.ipynb 3
from .stata import stata_formatted
from .stata_more import IndexVar

# %% ../nbs/06_pandas.ipynb 6
def _better_dataframe(hdl, var, obs, selectvar, valuelabel, missingval):
    import pandas as pd
    with IndexVar() as idx_var:
        data = hdl.getAsDict(var, obs, selectvar, valuelabel, missingval)
        if not data:
            return pd.DataFrame()
    
        if idx_var in data:
            idx = data.pop(idx_var)
        else:
            temp_var = [idx_var, selectvar] if selectvar else idx_var
            idx = hdl.getAsDict(temp_var, obs, selectvar, valuelabel, missingval).pop(idx_var)
        idx = pd.array(idx, dtype='int64')

        return pd.DataFrame(data=data, index=idx)

# %% ../nbs/06_pandas.ipynb 17
def _simple_dataframe_from_stata(stfr, var, valuelabel, missingval):
    from pystata import stata
    if stfr is None:
        df = stata.pdataframe_from_data(var=var, valuelabel=valuelabel, missingval=missingval)
    else:
        df = stata.pdataframe_from_frame(stfr, var=var, valuelabel=valuelabel, missingval=missingval)
    df.index += 1
    return df

# %% ../nbs/06_pandas.ipynb 20
def better_dataframe_from_stata(stfr, var, obs, selectvar, valuelabel, missingval, sformat):
    import numpy as np
    import pandas as pd
    import sfi
    hdl = sfi.Data if stfr is None else sfi.Frame.connect(stfr)
    custom_index_not_needed = obs is None and not selectvar
    if custom_index_not_needed:
        df = _simple_dataframe_from_stata(stfr, var, valuelabel, missingval)
    else:
        if hdl.getObsTotal() <= 0:
            return pd.DataFrame()
        df = _better_dataframe(hdl, var, obs, selectvar, valuelabel, missingval)
    if sformat:
        for v in list(df.columns):
            if hdl.isVarTypeString(v) or (valuelabel and missingval==np.NaN
                                          and pd.api.types.is_string_dtype(df[v])):
                continue
            v_format = hdl.getVarFormat(v)
            if missingval != np.NaN and pd.api.types.is_string_dtype(df[v]):
                def format_value(x):
                    return stata_formatted(x, v_format) if type(x)!=str else x
            else:
                def format_value(x):
                    return stata_formatted(x, v_format)
            df[v] = df[v].apply(format_value)
    return df

# %% ../nbs/06_pandas.ipynb 21
def better_pdataframe_from_data(var=None, obs=None, selectvar=None, valuelabel=False, missingval=None, sformat=False):
    import numpy as np
    if missingval is None:
        missingval = np.NaN
    return better_dataframe_from_stata(None, var, obs, selectvar, valuelabel, missingval, sformat)

# %% ../nbs/06_pandas.ipynb 22
def better_pdataframe_from_frame(stfr, var=None, obs=None, selectvar=None, valuelabel=False, missingval=None, sformat=False):
    import numpy as np
    if missingval is None:
        missingval = np.NaN
    return better_dataframe_from_stata(stfr, var, obs, selectvar, valuelabel, missingval, sformat)
