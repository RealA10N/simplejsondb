class Database:

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
