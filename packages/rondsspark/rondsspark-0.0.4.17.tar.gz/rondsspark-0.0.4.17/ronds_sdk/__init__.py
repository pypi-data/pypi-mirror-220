"""
RondsSpark SDK for Python3
"""
import sys
import warnings

if sys.version_info.major == 3:
    if sys.version_info.minor <= 6:
        warnings.warn(
            'This version of SDK has not been sufficiently tested on '
            'Python %s.%s. You may encounter bugs or missing features.' %
            (sys.version_info.major, sys.version_info.minor))
        pass
else:
    raise RuntimeError(
        'The SDK for Python is only supported on Python3. '
        'It is not supported on Python [%s].' % (str(sys.version_info))
    )
from ronds_sdk.dataframe.pvalue import PCollection
from ronds_sdk import logger_config
from ronds_sdk.options.pipeline_options import PipelineOptions
from ronds_sdk.transforms.ronds import *
from ronds_sdk.pipeline import Pipeline
from ronds_sdk.templates import *

Options = PipelineOptions

logger_config.config()


