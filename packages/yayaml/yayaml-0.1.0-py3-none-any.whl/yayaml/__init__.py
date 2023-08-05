"""
yayaml:

"""
# Public interface
from ._constructors import construct_from_func
from ._exceptions import ConstructorError, RepresenterError
from ._io import load_yml, write_yml, yaml_dumps, yaml_dumps_plain
from ._representers import build_representer
from ._yaml import (
    add_constructor,
    add_representer,
    is_constructor,
    is_representer,
    yaml,
    yaml_safe,
    yaml_unsafe,
)

# NOTE The representers and constructors submodules need to be imported,
#      otherwise there will be no registrations

__version__ = "0.1.0"
