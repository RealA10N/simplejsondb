import os
import json
import typing
import atexit
import copy


class Database:

    EMPTY_DB = None

    def __init__(self,
                 name: str,
                 extention: str = 'json',
                 folder: str = None,

                 save_at_exit: bool = True,
                 ):

        if folder is None:
            # If folder path is not given, generates the path
            folder = os.path.join(os.getcwd(), 'db')

        self.name = name
        self.extention = extention
        self.folder = folder

        if os.path.isfile(self.path):
            self._data = self.__load()
        else:
            # If database file doesn't exist yet (and there is no data to load),
            # sets the data to the default empty value.
            self.clear()

        if save_at_exit:
            atexit.register(self.save)

    def __str__(self,):
        """ Returns a string that represents the current database instance. """
        return f"<{self.__class__.__name__} {str(self._data)}>"

    def __eq__(self, other):
        """ Comperes the data in the database to the given data, and returns
        `True` only if they are equal. """
        return self._data == other

    def __ne__(self, other):
        """ Comperes the data in the database to the given data, and returns
        `True` only if they are not equal. """
        return not self == other  # returns the opposite of __eq__

    def __getitem__(self, item):
        """ Implementation of getting data from the database using brackets.
        For example: `x = db[3]`. """
        return self._data[item]

    def __setitem__(self, item, value):
        """ Implementation of setting and updating the data in the database
        using brackets. For example: `db[2] = 'hello!'` """
        self._validate_data(value)
        self._data[item] = value

    def __len__(self,):
        """ Returns the number of values in the database. Uses the `count`
        method. """
        return self.count()

    def __load(self,):
        """ Loads the database from the database path, and returns the loads
        json data. Called when the database is constructed, and when the
        database file exists. """

        with open(self.path, 'r') as file:
            return json.load(file)

    def save(self,
             indent: typing.Optional[int] = 4,
             ):
        """ Saves the data in the database into the local storage, as a json
        file. """

        # Creates the folders that will contain the json files (if they
        # don't exist yet)
        os.makedirs(self.folder, exist_ok=True)

        # Actually saves the data to the json file
        with open(self.path, 'w') as file:
            json.dump(self._data, file, indent=indent)

    def clear(self,):
        """ Removes all the elements from the database. """
        self._data = self.EMPTY_DB

    def count(self,):
        """ Returns the number of values in the database. """
        return len(self._data)

    @property
    def path(self,):
        """ The path to the json file that contains the database. """
        return os.path.join(self.folder, f'{self.name}.{self.extention}')

    def set(self, data):
        """ Recives some data, and sets it to be the data that is stored in
        the database.

        Note: Using this method is not recommended. This method will replace
        the saved data in the database with the new data, and the old data will
        be erased. """

        self._validate_data(data)
        self._data = data

    def copy(self,):
        """ Returns a copy of the data in the database. """
        return copy.deepcopy(self._data)

    def _validate_data(self, data):
        """ The database saves its data locally using the `json` format.
        This format supports only the basic data types, which are:
        1.  string (`str`)
        2.  number (`float` or `int`. Not `complex`!)
        3.  boolean (`bool`)
        4.  null (`None`)
        5.  dictionary (`dict`)
        6.  array (`list`)

        This method recives some data, and raises an error only if the data
        cannot be converted to the basic json types. """

        # Checks the data type
        if not isinstance(data, (str, float, int, bool, type(None), dict, list)):
            raise TypeError(f"Data type {type(data)} is not supported")

        if isinstance(data, dict):
            # If dictionary, checks if all dictionary keys are strings.
            # Also, calls this method for each value ('cell') in the dictionary
            # recursively.

            for key in data:
                if not isinstance(key, str):
                    raise TypeError(
                        f"Only string dictionary key are supported (not {type(data)})"
                    )

                self._validate_data(data[key])

        if isinstance(data, list):
            # If list, calls this method for each value ('cell') in the list
            # recursively.

            for value in data:
                self._validate_data(value)
