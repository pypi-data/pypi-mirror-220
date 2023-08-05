import pandas
import json
from os import path
from ml4proflow_mods.io.exceptions import UnknownFileExtension


def write_file_helper(data: pandas.DataFrame,
                      filename: str,
                      write_metadata: bool,
                      parser_options: dict) -> None:
    p, basename = path.split(filename)
    ext = ".".join(basename.rsplit('.', maxsplit=2)[1:]).lower()
    if 'csv' in ext:
        data.to_csv(filename, **parser_options)
    elif 'json' in ext:
        data.to_json(filename, **parser_options)
    elif 'h5' in ext:
        data.to_hdf(filename, **parser_options)
    else:
        raise UnknownFileExtension(f'Filename: {filename}, parsed ext {ext}')
    if write_metadata:
        meta_filename = "".join([filename[0:-len(ext)], '.mjson'])
        meta = write_meta_data(meta_filename, data.attrs)


def write_meta_data(filename: str, meta: dict) -> None:
    with open(filename, 'w') as f:
        json.dump(meta, f)

# elif filename.endswith(".mat"):
# tmp = loadmat(filename)
# tmp = numpy.array(tmp['StromBox_Werte'])
# tmp.byteswap().newbyteorder('=')
# names = ['time', ...]
# df = pandas.DataFrame({names[i]: tmp[i, :] for i in range(0, len(names))})
# delimiter=';', decimal=','
