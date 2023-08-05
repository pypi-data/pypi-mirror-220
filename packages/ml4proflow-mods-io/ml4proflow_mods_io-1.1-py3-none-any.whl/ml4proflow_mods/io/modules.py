from __future__ import annotations
from typing import Any, Union
import os
import glob
import gettext
from os import path
from ml4proflow.modules import SourceModule, SinkModule, ExecutableModule, DataFlowManager
from ml4proflow_mods.io.file_readers import read_file_helper
from ml4proflow_mods.io.file_writers import write_file_helper


# Localisation
t = gettext.translation(path.splitext(path.basename(__file__))[0],
                        path.dirname(path.abspath(__file__))+"/locales")
_ = t.gettext


# todo recursive option
class FileSourceModule(SourceModule, ExecutableModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SourceModule.__init__(self, dfm, config)
        ExecutableModule.__init__(self, dfm, config)
        self.config.setdefault('file', "")
        self.config.setdefault('read_metadata', False)
        self.config.setdefault('parser_options', {})

    def execute_once(self) -> None:
        df = read_file_helper(self.config['file'],
                              self.config['read_metadata'],
                              self.config['parser_options'])
        # TODO: move to base
        df.attrs["chain"].append(self.__class__.get_module_ident())
        self._push_data(self.config['channels_push'][0], df)

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {"name": _("File source"),
                "categories": ["IO"],
                "jupyter-gui-cls": "ml4proflow_jupyter.widgets.BasicWidget",
                "jupyter-gui-override-settings-type": {"file": "file"},
                "html-description": _("""
                Read data from file.
                """)
                }


class FileSinkModule(SinkModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SinkModule.__init__(self, dfm, config)
        self.config.setdefault('file', "")
        self.config.setdefault('parser_options', {})
        self.config.setdefault('write_metadata', False)

    def on_new_data(self, name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        write_file_helper(data, self.config['file'],
                                self.config['write_metadata'],
                                self.config['parser_options'])

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {"name": _("File sink"),
                "categories": ["IO"],
                "jupyter-gui-cls": "ml4proflow_jupyter.widgets.BasicWidget",
                "jupyter-gui-override-settings-type": {"file": "file"},
                "html-description": _("""
                Write data into file.
                """)
                }


# todo recursive option
class DirectoryFileSourceModule(SourceModule, ExecutableModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SourceModule.__init__(self, dfm, config)
        ExecutableModule.__init__(self, dfm, config)
        self.config.setdefault('directory', "./")
        self.config.setdefault('read_metadata', False)
        self.config.setdefault('glob', "*.csv")
        self.config.setdefault('parser_verbose', False)
        self.config.setdefault('parser_options', {})
        self.update_file_list()
        self.current_file_id = 0

    # todo remove unknown extensions
    def update_file_list(self) -> None:
        target_dir = self.config['directory']
        try:
            #self.files = ["".join([target_dir, f]) for f in os.listdir(target_dir)]
            self.files = glob.glob("".join([target_dir,self.config['glob']])) 
            # remove all directories:
            self.files = [f for f in self.files if os.path.isfile(f)]
        except FileNotFoundError:
            self.files = []
        self.current_file_id = 0

    def update_config(self, k: str, v: Any) -> None:
        SourceModule.update_config(self, k, v)
        if k=='directory':
            self.update_file_list()

    def execute_once(self) -> None:
        print("Processing %s files (%s)" % (len(self.files), self.config['directory']))
        if self.current_file_id < len(self.files):
            df = read_file_helper(self.files[self.current_file_id],
                                  self.config['read_metadata'],
                                  self.config['parser_options'],
                                  verbose=self.config['parser_verbose'])
            # TODO: move to base
            df.attrs["chain"].append(self.__class__.get_module_ident())
            self._push_data(self.config['channels_push'][0], df)
            self.current_file_id += 1

    def get_file_count(self) -> int:
        return len(self.files)

    def get_remaining_file_count(self) -> int:
        return self.get_file_count()-self.current_file_id

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {"name": _("Directory source"),
                "categories": ["IO"],
                "jupyter-gui-cls": "ml4proflow_jupyter.widgets.BasicWidget",
                "jupyter-gui-override-settings-type": {"directory": "file"},
                "html-description": _("""
                    Read data from directory.
                    """)
                }

class DirectoryFileSinkModule(SinkModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SinkModule.__init__(self, dfm, config)
        self.config.setdefault('directory', "./")
        self.config.setdefault('write_metadata', False)
        self.config.setdefault('parser_verbose', False)
        self.config.setdefault('parser_options', {})

    def on_new_data(self, name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        if 'source_name' not in data.attrs:
            print("Error: There is no 'source_name' in the metadata")
            print("DirectoryFileSinkModule is not able to guess the target filename (I will not write anything to the filesystem)")
            return
        # TODO cklarhor: use config dict!
        if "segment" in data.attrs:
            filename = "%s_%s" % (data.attrs["segment"],data.attrs['source_name'])
        else:
            filename = data.attrs['source_name']
        target_file = "%s/%s" %(self.config['directory'].rstrip(os.sep), filename)
        print("DirectoryFileSinkModule: Write to '%s'" % target_file)
        write_file_helper(data, target_file,
                                self.config['write_metadata'],
                                self.config['parser_options'])

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {"name": _("Directory sink"),
                "categories": ["IO"],
                "jupyter-gui-cls": "ml4proflow_jupyter.widgets.BasicWidget",
                "jupyter-gui-override-settings-type": {"directory": "file"},
                "html-description": _("""
                    Write data into directory.
                    """)
                }
