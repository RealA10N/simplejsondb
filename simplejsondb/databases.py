import os
import json
import typing
import atexit
import copy

# pylint: disable=unsubscriptable-object
JsonSupportedTypes = typing.Union[
    None,
    str,
    float,
    int,
    bool,
    typing.List['JsonSupportedTypes'],
    typing.Dict[str, 'JsonSupportedTypes'],
]


class Database:
    """ The most basic json database available. """

    DB_TYPE = None

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
            self.set(self.__load())
        else:
            # If database file doesn't exist yet (and there is no data to load),
            # sets the data to the default empty value.
            self.clear()

        if save_at_exit:
            atexit.register(self.save)

    # - - M A G I C - M E T H O D S - - #

    def __str__(self,) -> str:
        """ Returns a string that represents the current database instance. """
        return f"{self.__class__.__name__}({str(self._data)})"

    def __eq__(self, other) -> bool:
        """ Comperes the data in the database to the given data, and returns
        `True` only if they are equal. """
        return self._data == other

    def __ne__(self, other) -> bool:
        """ Comperes the data in the database to the given data, and returns
        `True` only if they are not equal. """
        return not self.__eq__(other)

    def __getitem__(self, item):
        """ Implementation of getting data from the database using brackets.
        For example: `x = db[3]`. """
        return self._data[item]

    def __setitem__(self, key, value: JsonSupportedTypes):
        """ Implementation of setting and updating the data in the database
        using brackets. For example: `db[2] = 'hello!'` """
        self._validate_data(value)
        self._data[key] = value

    def __iter__(self,):
        """ Iterate (loop over) the database. """
        return self._data.__iter__()

    def __len__(self,) -> int:
        """ Returns the number of values in the database. Uses the `count`
        method. """
        return self.count()

    # - - G E N E R A L - M E T H O D S - - #

    def count(self,) -> int:
        """ Returns the number of values in the database. """
        return len(self._data)

    def set(self, data: JsonSupportedTypes):
        """ Recives some data, and sets it to be the data that is stored in
        the database.

        Note: Using this method is not recommended. This method will replace
        the saved data in the database with the new data, and the old data will
        be erased. """

        # pylint: disable=isinstance-second-argument-not-valid-type

        if self.DB_TYPE is not None and not isinstance(data, self.DB_TYPE):
            raise TypeError(
                f"The '{self.__class__.__name__}' object only supports '{self.DB_TYPE.__name__}' (not {type(data)})"
            )

        self._validate_data(data)
        self._data = data

    def clear(self,) -> None:
        """ Removes all the elements from the database. """

        # If the database type is callable (for example: list, dict, etc),
        # creates a new instance of the object and saves it in the database.
        # Otherwise, saves the database type as the data in the database.

        if callable(self.DB_TYPE):
            self._data = self.DB_TYPE()  # pylint: disable=not-callable

        else:
            self._data = self.DB_TYPE

    def copy(self,) -> JsonSupportedTypes:
        """ Returns a copy of the data in the database. """
        return copy.deepcopy(self._data)

    # - - D A T A B A S E - M E T H O D S - - #

    def __load(self,) -> JsonSupportedTypes:
        """ Loads the database from the database path, and returns the loads
        json data. Called when the database is constructed, and when the
        database file exists. """

        with open(self.path, 'r') as file:
            return json.load(file)

    def save(self,
             indent: typing.Optional[int] = 4,
             ) -> None:
        """ Saves the data in the database into the local storage, as a json
        file. """

        # Creates the folders that will contain the json files (if they
        # don't exist yet)
        os.makedirs(self.folder, exist_ok=True)

        # Actually saves the data to the json file
        with open(self.path, 'w') as file:
            json.dump(self._data, file, indent=indent)

    @property
    def path(self,) -> str:
        """ The path to the json file that contains the database. """
        return os.path.join(self.folder, f'{self.name}.{self.extention}')

    def _validate_data(self, data: JsonSupportedTypes):
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


class ListDatabase(Database):
    """ Same as the basic `Database` object, but with more methods to better
    support a list database. """

    DB_TYPE = list

    def append(self, data) -> None:
        """ Adds the given data at the end of the database list. """
        self._validate_data(data)
        self._data.append(data)

    def extend(self, iterable: typing.Iterable) -> None:
        """ Add the elements of a given list (or any iterable), to the end of
        the database list. """
        data = list(iterable)
        self._validate_data(data)
        self._data.extend(data)

    def index(self, element) -> int:
        """ Returns the index of the first element with the specified value
        from the database. """
        return self._data.index(element)

    def insert(self, position: int, element) -> None:
        """ Adds an element at the specified position to the database. """
        self._validate_data(element)
        self._data.insert(position, element)

    def pop(self, position: int) -> JsonSupportedTypes:
        """ Removes and returns the element at the specified position from
        the database. """
        return self._data.pop(position)

    def remove(self, element) -> None:
        """ Removes the first item with the specified value from the
        database. """
        return self._data.remove(element)

    def reverse(self,) -> None:
        """ Reverses the order of the database list. """
        self._data.reverse()

    def sort(self,) -> None:
        """ Sorts the database list. """
        self._data.sort()


class DictDatabase(Database):
    """ Same as the basic `Database` object, but with more methods to better
    support a dict database. """

    DB_TYPE = dict

    def __check_valid_key(self, key) -> None:
        """ Recives a key to the database dictionary, and raises an error only
        if the key is invalid. """

        if not isinstance(key, str):
            raise TypeError(
                f"The '{self.__class__.__name__}' only supports string keys (not {type(key)})"
            )

    def __setitem__(self, key: str, value: JsonSupportedTypes) -> None:
        """ Implementation of setting and updating the data in the database
        using brackets. For example: `db['hi'] = 'hello!'` """

        self.__check_valid_key(key)
        super().__setitem__(key, value)

    def get(self, key: str, default=None,) -> JsonSupportedTypes:
        """ Returns the value of the specified key from the database. If the
        given key doesn't exist in the database, returns the given default
        value. """
        return self._data.get(key, default)

    def items(self,) -> list:
        """ Returns a list containing a tuple for each key value pair in the
        database.  """
        return self._data.items()

    def keys(self,) -> list:
        """ Returns a list containing the database's keys. """
        return self._data.keys()

    def pop(self, key: str, default: JsonSupportedTypes = None) -> JsonSupportedTypes:
        """ Removes the element with the specified key from the database, and
        returns it. If the element doesn't exist in the database, raises a
        TypeError. If a default value is provided, returns it instead of rasing
        an error. """
        return self._data.pop(key, default)

    def popitem(self,) -> JsonSupportedTypes:
        """ Removes the item that was last inserted into the database. In
        versions before 3.7, will remove and return a random item from the
        dictionary. """
        return self._data.popitem()

    def setdefault(self, key: str, default: JsonSupportedTypes = None) -> JsonSupportedTypes:
        """ Returns the value of the item with the specified key from the
        database. If the key does not exist, inserts the key with the default
        value. """
        return self._data.setdefault(key, default)

    def update(self, iterable: typing.Iterable) -> None:
        """ Inserts the specified items to the database dictionary. The item
        can be a dictionary, or an iterable object with key value pairs. """

        data = dict(iterable)
        for key in data:
            self.__check_valid_key(key)

        self._validate_data(data)
        self._data.update(data)

    def values(self,) -> list:
        """ Returns a 'view' object that contains the values of the database
        dictionary, as a list. The 'view' object will reflect any changes done
        to the dictionary database. """
        return self._data.values()
