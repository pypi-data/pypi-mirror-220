"""
Basic
"""
__version__ = '0.2.3'

__autogen__ = """
mkinit ~/code/kwutil/kwutil/__init__.py --lazy_loader --noattr
mkinit ~/code/kwutil/kwutil/__init__.py --noattr
"""

import sys

if sys.version_info[0:2] >= (3, 7):

    import lazy_loader
    __getattr__, __dir__, __all__ = lazy_loader.attach(
        __name__,
        submodules={
            'copy_manager',
            'partial_format',
            'slugify_ext',
            'util_environ',
            'util_eval',
            'util_json',
            'util_locks',
            'util_parallel',
            'util_path',
            'util_pattern',
            'util_progress',
            'util_resources',
            'util_time',
            'util_windows',
            'util_yaml',
        },
        submod_attrs={},
    )

else:
    # Cant do lazy loading in 3.6
    from kwutil import copy_manager
    from kwutil import partial_format
    from kwutil import slugify_ext
    from kwutil import util_environ
    from kwutil import util_eval
    from kwutil import util_json
    from kwutil import util_locks
    from kwutil import util_parallel
    from kwutil import util_path
    from kwutil import util_pattern
    from kwutil import util_progress
    from kwutil import util_resources
    from kwutil import util_time
    from kwutil import util_windows
    from kwutil import util_yaml


__all__ = ['copy_manager', 'partial_format', 'slugify_ext', 'util_environ',
           'util_eval', 'util_json', 'util_locks', 'util_parallel',
           'util_path', 'util_pattern', 'util_progress', 'util_resources',
           'util_time', 'util_windows', 'util_yaml']
