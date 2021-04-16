def templatematch(template,obj):
    ret = True
    for key,val in template.items():
        if key not in obj:
            ret = False
            break
        if isinstance(val,dict):
            cret = templatematch(val, obj[key])
        else:
            cret = obj[key] == val
        if not cret:
            ret = False
            break
    return ret
