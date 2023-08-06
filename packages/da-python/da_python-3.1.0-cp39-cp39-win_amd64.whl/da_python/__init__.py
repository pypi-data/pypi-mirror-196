from __future__ import absolute_import

from .c_lib_wrap import (
    is_built_with_ort,
    is_built_with_paddle,
    is_built_with_openvino,
    create,
)

from . import serving
from . import c_lib_wrap as da_python
from .code_version import *

__version__ = version
__git_version__ = git_version
