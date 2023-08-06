def reverse(param):
    """Reversing a list"""
    if isinstance(param, list):
        newver = []
        a = len(param) - 1
        for item in range(len(param)):
            newver.insert(item, param[a])
            a -= 1
        return newver
        """Reversing a tuple"""
    elif isinstance(param, tuple):
        newver = []
        a = len(param) - 1
        for item in range(len(param)):
            newver.insert(item, param[a])
            a -= 1
        return tuple(newver)

        """Reversing a dictionary"""
    elif isinstance(param, dict):
        dict_ = []
        dict_to_list = list(param.items())
        a = len(dict_to_list) - 1
        for item in range(len(dict_to_list)):
            dict_.insert(item, dict_to_list[a])
            a -= 1
        return dict(dict_)

        """Reversing a string"""
    elif isinstance(param, str):
        newver = ""
        a = len(param) - 1
        for item in range(len(param)):
            newver += param[a]
            a -= 1
        return newver.strip()
        """Reversing a integer"""
    elif isinstance(param, int):
        newver = ""
        a = len(str(param)) - 1
        for item in range(len(str(param))):
            newver += str(param)[a]
            a -= 1
        return int(newver)
    elif param is not None:
        newver = ""
        a = len(str(param)) - 1
        for item in range(len(str(param))):
            newver += str(param)[a]
            a -= 1
        return str(newver)
    else:
        return "Eerie said | ", param, " is not a list, tuple, dict, str or int"
