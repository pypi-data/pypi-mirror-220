class FindValue:
    def __init__(self):
        pass

    def __str__(self) -> str:
        pass

    def find_keys_value(self, adict, key):
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
