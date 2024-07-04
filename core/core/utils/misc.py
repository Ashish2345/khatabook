import yaml

def yaml_coerce(value: str) -> dict:
    '''
    Convert string nested dict values to proper python dictionary
    
    Eg: "{'foo': 'bar', 'bar':'foo'}" to python dict

    Useful because sometimes we need to stringify settings this way (like in Dockerfiles)
    '''
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', loader=yaml.SafeLoader)['dummy']
    return value
