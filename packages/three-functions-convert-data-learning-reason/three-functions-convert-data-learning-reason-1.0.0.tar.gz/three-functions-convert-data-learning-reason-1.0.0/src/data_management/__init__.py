from importlib import resources


try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Version of the realpython-reader package
__version__ = "1.0.0"

_cfg = tomllib.loads(resources.read_text("data_management", "config.toml"))
