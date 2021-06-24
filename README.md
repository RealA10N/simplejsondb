![Simple Json Database](/assets/banner.png)

Do you need a simple, small, and very easy to use local database? You have come
to the right place! with _simplejsondb_ you can create a simple JSON database with
only one line of code, and we will take care of the rest!

## A basic example

```python
from simplejsondb import Database

# If database named 'translations' doesn't exist yet, creates a new empty dict database
translations = Database('translations.json', default=dict())

# Now, we can treat the database instance as a dictionary!
translations.data['Hello'] = 'Hola'
translations.data['Goodbye'] = 'Adiós'
print(translations.data.values())   # dict_values(['Hola', 'Adiós'])

# The database will automatically save the changes when the program exits
```

After running the code above for the first time, a file named `translations.json`
will be automatically created under the current working directory. Then, we will
be able to use the database inside other scripts, and treat it as a dictionary:

```python
from simplejsondb import Database

# loads the previously saved translations database
translations = Database('translations.json')

# Again, we treat the 'translations' instance as a dictionary
print(f"Hello in Spanish is {translations.data['Hello']}!")
# This will output: Hello in Spanish is Hola!

# We can also use the built in dictionary methods
for english, spanish in translations.data.items():
    print(f"{english} in Spanish is {spanish}!")

# This will output:
# Hello in Spanish is Hola!
# Goodbye in Spanish is Adiós!
```

## Installation

The simplest way to install _simplejsondb_ is by using `pip`. Just run the following
command in your terminal:

```console
$ (sudo) pip install simplejsondb
```

You can also clone the [Github repo](https://github.com/RealA10N/simplejsondb),
download the latest release from [Github](https://github.com/RealA10N/simplejsondb/releases)
or directly from [PyPI](https://pypi.org/project/simplejsondb/#files). Then, unzip
the files (if they are zipped), and use the following command to install the package:

```console
$ (sudo) python setup.py install
```

If the command above didn't work, make sure that you have the `setuptools` package
installed using:

```console
$ (sudo) pip install setuptools
```

## Methods

### Database(path, default=None, overwrite=False, save_at_exit=True)

The constructor of the `Database` instance. Receives a path to a `JSON` file, and
tries to load it. If the file doesn't exist, loads the default data that is passed
using the `default` argument.

### Arguments

- **path (str):** The path to the json database file.
- **default:** The default data that will be loaded if the file doesn't exist yet.
- **overwrite (bool):** If `True`, loads the `default` without checking if the file exists.
- **save_at_exit (bool):** If `True` (default), will automatically dump the database
    into storage when the program exits.


### Database.save(**additional)

By default, the database is loaded from the local storage when the instance is
created. It is then saved in the memory, until the program exits - and only then
the new and updated data is saved back in the local storage. By using the
`Database.save()` method, you can save the database into the local storage before
the program exists, in any given point.

#### Additional arguments

The `save` method supports receiving additional keyword arguments that are directly
passed into the `json.dump` function. One useful argument can be `indent` that is
a non-negative integer that sets the indention level of the dumped json file. For
more information, check out the [json module documentation].

### Database.load()

Loads the data from the `json` file into the instance. Overwrites previous data that was
saved under the `.data` property.

## Properties

### Database.path

A property that contains the path to the database JSON file.

### Database.folder

A property that stores the absolute path to the directory where the database json
file lives in.

[json module documentation]: https://docs.python.org/3/library/json.html#json.dump
