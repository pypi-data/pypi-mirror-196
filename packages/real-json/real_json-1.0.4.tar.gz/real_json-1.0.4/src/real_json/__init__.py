from real_json.GetWrappedJson import GetWrappedJson

__version__ = "1.0.3"


def ify(obj):
    if isinstance(obj, GetWrappedJson):
        return obj
    
    return GetWrappedJson(obj)
