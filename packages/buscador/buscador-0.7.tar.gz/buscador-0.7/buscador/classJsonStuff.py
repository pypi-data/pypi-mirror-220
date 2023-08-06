class JsonStuff:
    def __init__(self):
        pass

    def __str__(self) -> str:
        pass

    def find_keys_value(adict: dict, key: str):
        """Returns value of a given key, even if nested

        Args:
            adict (dict): target dictionary
            key (str): target dictionary key

        Returns:
            Value of target dictionary key
        """
        stack = [adict]
        while stack:
            d = stack.pop()
            if key in d:
                return d[key]
            for v in d.values():
                if isinstance(v, dict):
                    stack.append(v)
                if isinstance(v, list):
                    stack += v

    def get_paths(my_dict: dict, path=None):
        """
        Get paths for nested keys in dictionaries.
        Args:
            my_dict (dict): Target dictionary.
            path (list, optional): Defaults to None.
        """
        if path is None:
            path = []
        for k, v in my_dict.items():
            newpath = path + [k]
            if isinstance(v, dict):
                for u in JsonStuff.get_paths(v, newpath):
                    yield u
            else:
                yield newpath, v
