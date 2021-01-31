![Simple Json Datbase](/assets/banner.png)

Do you need a simple, small, and very easy to use local database? You have come to the right place!
with _simplejsondb_ you can create a simple JSON database with only one line of code, and we will take care of the rest!

## A basic example

```python
from simplejsondb import DictDatabase

# If database named 'translations' doesn't exist yet, creates a new empty dict database
translations = DictDatabase('translations')

# Now, we can treat the database instance as a dictionary!
translations['Hello'] = 'Hola'
translations['Goodbye'] = 'Adiós'

# The database will automatically save the changes when the program exits
```

After running the code above for the first time, a file named `translations.json` will be automatically created under the current working directory. Then, we will be able to use the database inside other scripts, and treat it as a dictionary:

```python
from simplejsondb import DictDatabase

# loads the previously saved translations database
translations = DictDatabase('translations')

# Again, we treat the 'translations' instance as a dictionary
print(f"Hello in Spanish is {translations['Hello']}!")
# This will output: Hello in Spanish is Hola!

# We can also use the built in dictionary methods
for english, spanish in translations.items():
    print(f"{english} in Spanish is {spanish}!")

# This will output:
# Hello in Spanish is Hola!
# Goodbye in Spanish is Adiós!
```

## Special Objects and Methods

The *simplejsondb* module is designed to behave as close as possible to basic Python objects.
To do that, in addition to the `Database` object, there are another two objects that *simplejsondb* provides: `ListDatabase` and `DictDatabase`.
`ListDatabase` and `DictDatabase` behave exactly as the regular `Database` object, but in addition, you can use the built in python methods for lists and dictionaries, like `ListDatabase.append(data)` or `DictDatabase['Hello'] = Hola`.

**In addition, the `Database`, `ListDatabase` and `DictDatabase` objects share a few special methods:**

### Database.set(data)

There is a small problem while using the `Database` instance. When you try to create a list or a dictionary, it automatically loads the database from the local storage. If you want to clear the saved data, and overwrite it with new data, you should use the `.set(data)`  method!

It is also possible to use the **`Database.clear()`** method, to reset the database. This method will set the database data to `None` if the object is the default `Database` object,  `[]` if the object is a `ListDatabase`, and `{}` if the object is a `DictDatabae`.

### Database.copy()

Returns a copy of the data in the database. Plain and simple!

### Database.save()

By default, the database is loaded from the local storage when the instance is created. It is then saved in the memory, until the program exits - and only then the new and updated data is saved back in the local storage. By using the `Database.save()` method, you can save the database into the local storage before the program exists, in any given point.

### Database.path

`Database.path` is a property that contains the path to the database JSON file.