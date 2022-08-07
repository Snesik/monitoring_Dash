import yaml


def read_yaml(path: str):
    """Загрузить из yaml"""
    with open(path, 'r') as c:
        return yaml.safe_load(c)
