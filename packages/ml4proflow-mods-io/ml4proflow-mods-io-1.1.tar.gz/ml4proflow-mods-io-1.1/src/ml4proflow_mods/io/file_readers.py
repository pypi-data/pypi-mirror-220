import pandas
import json
from os import path
from ml4proflow_mods.io.exceptions import UnknownFileExtension

def read_file_helper(filename: str,
                     read_metadata: bool,
                     parser_options: dict,
                     verbose: bool = False) -> pandas.DataFrame:
    p, basename = path.split(filename)
    ext = ".".join(basename.rsplit('.', maxsplit=2)[1:]).lower()
    if ext in ['csv', 'csv.gz', 'csv.bz2']:
        df = pandas.read_csv(filename, **parser_options)
    elif ext in ['json', 'json.gz', 'json.bz2']:
        df = pandas.read_json(filename, **parser_options)
    elif ext in ['h5']:
        df = pandas.read_hdf(filename, **parser_options)
    else:
        raise UnknownFileExtension(f'Filename: {filename}, parsed ext {ext}')
    if read_metadata:
        meta_filename = "".join([filename[0:-len(ext)], 'mjson'])
        if path.exists(meta_filename):
            if verbose:
                print("Found metadata file")
            meta = read_meta_data(meta_filename)
            df.attrs.update(meta)
    df.attrs = {'source_name': basename,
                'source_fullname': filename,
                'source_cols': len(df.columns),
                'source_rows': len(df.index),
                'chain': []}
    if verbose:
        print("DF has %d rows and %d cols" % (len(df), len(df.columns)))
    return df

def read_meta_data(filename: str) -> dict:
    with open(filename) as f:
        return json.load(f)

# elif filename.endswith(".mat"):
# tmp = loadmat(filename)
# tmp = numpy.array(tmp['StromBox_Werte'])
# tmp.byteswap().newbyteorder('=')
# names = ['time', ...]
# df = pandas.DataFrame({names[i]: tmp[i, :] for i in range(0, len(names))})
# delimiter=';', decimal=','
