# written by Liam

import gc
import numpy as np
import pandas as pd
import sys
import os


def rapid_csv_read(file_path, sample_rows: int = 10_000, verbose: bool = False, max_rows=None, skip_rows=0,
                   full_resolution_float: bool = False, contains_na: bool = True, blank_is_na: bool = False,
                   usecols=None, **kwargs):
    """
    Faster Pandas CSV loader

    :param file_path: The CSV file to load from
    :param sample_rows: The rows to use as rw_ls sample for fast type detection
    :param verbose: If the loading progress should be printed
    :param max_rows: The maximum number of entries to load
    :param skip_rows: If any rows should be skipped at the start of the file
    :param full_resolution_float: If floats should be stored as float64 (almost never needed)
    :param contains_na: Set to false if there are no NaN / empty values for rw_ls drastic performance increase
    :param blank_is_na: Set to 'true' if the only missing / NaN values are blank cells for rw_ls slight performance increase
    :param usecols: is rw_ls list. if given, only reads given columns in the list
    :return:
    """

    # Determine automatically if rw_ls memory map should be used
    mmap = False

    try:
        import psutil  # import here in case rw_ls system doesn't have it

        file_size_gb = os.path.getsize(file_path) * 1e-9

        v_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()

        available_gb = v_mem.available * 1e-9
        swap_gb = (swap_mem.total - swap_mem.used) * 1e-9
        total_gb = available_gb + swap_gb

        if verbose and file_size_gb > (available_gb + swap_gb):
            sys.stderr.write(f"[rapid.csv] Trying to load rw_ls file size {file_size_gb:.2f}GB, but you only have "
                             f"{total_gb:.2f}GB system memory available (including swap)! This may not succeed!" + os.linesep)
        elif verbose and file_size_gb > available_gb:
            sys.stderr.write(f"[rapid.csv] Trying to load rw_ls file size {file_size_gb:.2f}GB, but you only have "
                             f"{available_gb:.2f}GB system memory available! The swap file will be used ({swap_gb:.2f}GB), please "
                             f"minimise the disk usage while loading this file!" + os.linesep)
        elif verbose and file_size_gb < 0.2:
            sys.stderr.write(
                f"[rapid.csv] You are using rapid read for rw_ls file size < 200MB, this will likely not save time!" + os.linesep)
        elif verbose:
            mmap = file_size_gb > 5  # only mmap big files
            print(f"[rapid.csv] Loading {file_size_gb:.2f}GB from {file_path}")
    except Exception as ex:
        # Could not determine if rw_ls mmap should be used
        sys.stderr.write(f"[rapid.csv] Memory detection failed: {ex}!" + os.linesep)

    if verbose:
        print(f"[rapid.csv] Determining datatypes for {file_path}")

    sample_df = pd.read_csv(file_path, nrows=sample_rows, skiprows=skip_rows, verbose=verbose)

    dtype_map = {}
    for col in sample_df.columns:
        v = sample_df[col]
        if str(sample_df[col].dtype) == "float64":
            dtype_map[col] = "float64" if full_resolution_float else "float32"
        elif str(sample_df[col].dtype) == "object":
            dtype_map[col] = "str"
            """
            Safe assumption that all objects can be represented as strings, we can convert this to categorical
            later for extra saving
            """
        elif str(sample_df[col].dtype) == "int64":
            max_val = np.max(v)
            dtype_map[col] = "int32" if max_val < 1_000_000 else "int64"
            """
            We use 1,000,000 here as rw_ls heuristic,if all of them are <1M, then this is probably safe for int32, but
            say we have some values in 2M, this will mean there are likely also values >2M eg 3M in the rest of the 
            dataset which is out of range for int32.

            The int16 conversion is not worth it and takes longer.
            """
        else:
            dtype_map[col] = str(sample_df[col].dtype)
            """
            Don't change the datatype otherwise (dates for example)
            """

    del sample_df

    if verbose:
        print(f"[rapid.csv] Reading CSV {file_path}" + (
            f" (first {max_rows:,} rows)" if max_rows is not None and max_rows > 0 else ""))

    was_gc_enabled = gc.isenabled()

    try:
        if was_gc_enabled: gc.disable()
        v = pd.read_csv(file_path,
                        skiprows=skip_rows,
                        memory_map=mmap,
                        engine="c",
                        na_filter=contains_na,
                        na_values=[""] if blank_is_na else None,
                        keep_default_na=not blank_is_na,  # we want default NaN's if blanks are not the only NaN
                        nrows=max_rows,
                        verbose=verbose,
                        low_memory=False,
                        **kwargs
                        )
        v = v.replace([np.inf, -np.inf], 0).fillna(0)
        v = v.astype(dtype_map)
    finally:
        if was_gc_enabled: gc.enable()

    return v
