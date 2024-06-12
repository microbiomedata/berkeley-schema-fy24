from typing import List, Type

from nmdc_schema.migrators.migrator_base import MigratorBase
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_unknown
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR23
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR4
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR53
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR21
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR129
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR31
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR9
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR19_and_PR70
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR2_and_PR24
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR10
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR3
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR176
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_PR176_to_PR104
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_X_to_PR192
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_PR104_to_PR195
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import migrator_from_PR195_to_unknown


def get_migrators() -> List[Type[MigratorBase]]:
    r"""
    Returns a list of migrators (i.e. classes) in the order in which they were designed to be run.

    >>> migrators = get_migrators()
    >>> type(migrators) is list and len(migrators) > 0  # the function returns a list
    True
    >>> from inspect import isclass
    >>> all(isclass(m) for m in migrators)  # each list item is a classes
    True
    >>> all(callable(getattr(m, "upgrade")) for m in migrators)  # each class has an `upgrade` method
    True
    """

    return [
        migrator_from_X_to_unknown.Migrator,
        migrator_from_X_to_PR23.Migrator,
        migrator_from_X_to_PR4.Migrator,
        migrator_from_X_to_PR53.Migrator,
        migrator_from_X_to_PR21.Migrator,
        migrator_from_X_to_PR129.Migrator,
        migrator_from_X_to_PR31.Migrator,
        migrator_from_X_to_PR9.Migrator,
        migrator_from_X_to_PR19_and_PR70.Migrator,
        migrator_from_X_to_PR2_and_PR24.Migrator,
        migrator_from_X_to_PR10.Migrator,
        migrator_from_X_to_PR3.Migrator,
        migrator_from_X_to_PR176.Migrator,
        migrator_from_PR176_to_PR104.Migrator,
        migrator_from_X_to_PR192.Migrator,
        migrator_from_PR104_to_PR195.Migrator,
        migrator_from_PR195_to_unknown.Migrator,
    ]
