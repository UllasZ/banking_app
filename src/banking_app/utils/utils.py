import hashlib

m = hashlib.sha1()


class Utils:

    @staticmethod
    def clean_list_of_dicts(data_array):
        new_data_array = []
        for column in data_array:
            for key, value in column.items():
                if isinstance(value, str):
                    """Removes binary string."""
                    value = value.replace("\x00", "")
                    column[key] = value.strip()

            new_data_array.append(column)
        return new_data_array



utils = Utils()
