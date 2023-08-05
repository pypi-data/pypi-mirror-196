from os.path import exists
from pyntree.errors import Error
import compress_pickle as pickle
import json

EXTENSIONS = {
    "txt": "txt",
    "pyn": "pyn",
    "pyndb": "pyn",
    "json": "json",
    **pickle.get_registered_extensions()
}
DEFAULT_FILETYPE = 'pyn'


def infer_filetype(data) -> str:
    if type(data) is str:
        if len(data.rsplit('.')) > 1:  # If filename has extension
            ext = data.rsplit('.')[-1]
            if ext in EXTENSIONS.keys():  # And it's a valid one
                return EXTENSIONS[ext]  # Then use that
    return DEFAULT_FILETYPE


class File:
    def __init__(
            self,
            data,
            filetype=None,
            autosave=False,
            save_on_close=False
    ) -> None:

        """
        Load a file for use with a Node object. If the filetype is unknown, 'pyn' will be used.
        Use switch_to_file to change the filename, as changing File.name will not update the file object.

        Filetype options:

        - pyn (Serialized data) (default)
        - bz2, gzip, lz4, lzma, None, pickle, zipfile (Compressed data of their respective types)
        - txt (plain text data)
        - json

        :param data: The filename or dictionary object
        :param filetype: The type of data stored/to store
        :param autosave: Save the file when Nodes are updated
        :param save_on_close: Whether to save the file when this object is destroyed (irrelevant if autosave = True)
        """
        self.autosave = autosave
        self.save_on_close = save_on_close
        self.file = None
        if type(data) is str:  # Helps a Data class work
            self.switch_to_file(data, filetype=filetype)
            self.data = self.read_data()  # Not to be confused with the data parameter
        else:
            self.data = data
            self.filetype = 'txt' if not filetype else filetype
            self.name = None

    # noinspection PyTypeChecker
    def read_data(self) -> dict:
        """
        :return: The data currently stored in the file
        """
        self.file.seek(0)
        if self.filetype == 'pyn':
            return pickle.loads(self.file.read(), None)
        elif self.filetype == 'json':
            return json.loads(self.file.read())
        elif self.filetype == 'txt':
            return eval(self.file.read())
        elif self.filetype in pickle.get_known_compressions():
            return pickle.loads(self.file.read(), self.filetype)

    # noinspection PyAttributeOutsideInit
    def switch_to_file(self, filename, filetype=None) -> None:
        """
        Closes the old file object (if it exists) and replaces it with a new one.
        :param filename: The name of the file to switch to
        :param filetype: The type of data stored in the file to switch to
        :return:
        """
        self.name = filename
        if self.file:  # Close open file if it exists
            self.file.close()
        if filetype is None:
            self.filetype = infer_filetype(filename)
        if not exists(filename):
            with open(filename, 'wb') as file:  # Create file in proper format if it doesn't exist
                if self.filetype in ('json', 'txt'):
                    file.write(b'{}')
                elif self.filetype == 'pyn':
                    file.write(pickle.dumps({}, None))
                else:
                    file.write(pickle.dumps({}, self.filetype))
        if self.filetype == 'pyn' or self.filetype in pickle.get_known_compressions():
            self.file = open(filename, 'rb+')
        else:
            self.file = open(filename, 'r+')

    def reload(self):
        """
        Sets the data object for the file to the data stored in the file
        :return:
        """
        self.data = self.read_data()

    # noinspection PyUnboundLocalVariable
    def save(self, filename=None) -> None:
        """
        Saves the data to the file
        :param filename: If set, the Node will save to the specified file and then reload its original file object
        """
        if filename:  # Only keeps 1 file in memory at a time
            old_filename = self.name
            self.switch_to_file(filename)
        elif not self.file and not filename:
            raise Error.FileNameUnset(
                "You have not specified a filename for this data. "
                "Try setting the filename parameter or use switch_to_file."
            )
        if self.filetype == 'pyn':
            to_write = pickle.dumps(self.data, None)
        elif self.filetype == 'json':
            to_write = json.dumps(self.data, sort_keys=True, indent=2)
        elif self.filetype == 'txt':
            to_write = str(self.data)
        elif self.filetype in pickle.get_known_compressions():
            to_write = pickle.dumps(self.data, self.filetype)
        self.file.seek(0)
        self.file.write(to_write)
        self.file.truncate()
        if filename and old_filename:  # If the old filename was None, then it can't be switched back to
            self.switch_to_file(old_filename)

    def __del__(self) -> None:
        """
        Garbage collector function for implementing save_on_close and properly closing the file object
        :return:
        """
        if 'file' in self.__dict__.keys():  # If file attribute was set
            if self.save_on_close:
                self.save()
            if self.file:
                self.file.close()
