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
