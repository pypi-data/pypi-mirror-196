"""Initial Module.

Source repository: https://github.com/aws/aws-sdk-pandas
Documentation: https://aws-sdk-pandas.readthedocs.io/

"""

import logging as _logging

from h10awswrnglr import (  # noqa
    athena,
    catalog,
    chime,
    cloudwatch,
    data_api,
    data_quality,
    dynamodb,
    emr,
    exceptions,
    lakeformation,
    mysql,
    neptune,
    opensearch,
    oracle,
    postgresql,
    quicksight,
    redshift,
    s3,
    secretsmanager,
    sqlserver,
    sts,
    timestream,
)
from h10awswrnglr.__metadata__ import __description__, __license__, __title__, __version__  # noqa
from h10awswrnglr._config import config  # noqa

__all__ = [
    "athena",
    "catalog",
    "chime",
    "cloudwatch",
    "emr",
    "data_api",
    "data_quality",
    "dynamodb",
    "exceptions",
    "opensearch",
    "oracle",
    "quicksight",
    "s3",
    "sts",
    "redshift",
    "lakeformation",
    "mysql",
    "neptune",
    "postgresql",
    "secretsmanager",
    "sqlserver",
    "config",
    "timestream",
    "__description__",
    "__license__",
    "__title__",
    "__version__",
]


_logging.getLogger("h10awswrnglr").addHandler(_logging.NullHandler())
