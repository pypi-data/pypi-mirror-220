from __future__ import annotations

## Import modules with only stdblit dependencies directly
from .context_managers import DictProtect, ListProtect, async_benchmark, benchmark
from .dict_utils import debug_dict, merge_dicts, update_dict, validate_dict
from .file_utils import crawl_dir, default_json_dir, export_json, ts
from .hash_utils import get_hash_from_str
from .time_utils import (
    datetime_as_dt,
    datetime_as_str,
    default_format as default_ts_format,
    get_ts,
    twelve_hour_format as ts_twelve_hour_format,
)
from .uuid_utils import (
    UUIDLength,
    first_n_chars,
    gen_uuid,
    get_rand_uuid,
    glob_uuid_lens,
    trim_uuid,
)

## Use try/except to import modules with dependencies
#  Keeps program from crashing when only a single module
#    is missing a depenency.
try:
    from . import diskcache_utils
except:
    pass
try:
    from . import httpx_utils
except:
    pass
try:
    from . import loguru_utils
except:
    pass
try:
    from . import msgpack_utils
except:
    pass

## Only import fastapi utils if fastapi and uvicorn are installed
try:
    from . import fastapi_utils
except:
    pass

from .context_managers import async_benchmark, benchmark
