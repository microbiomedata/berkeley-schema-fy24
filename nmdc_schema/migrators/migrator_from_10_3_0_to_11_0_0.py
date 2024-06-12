from nmdc_schema.migrators.migrator_base import MigratorBase
from nmdc_schema.migrators.partials.migrator_from_10_3_0_to_11_0_0 import get_migrators


class Migrator(MigratorBase):
    r"""
    Migrates a database between two schemas.

    Specifically, this migrator migrates a database that conforms to the "pre-Berkeley schema"
    into one that conforms to the "Berkeley schema".

    Reference: https://pypi.org/project/nmdc-schema/#history
    """

    _from_version = "10.3.0"
    _to_version = "11.0.0"  # a.k.a. the Berkeley schema

    def upgrade(self) -> None:
        r"""
        Migrates the database from conforming to the original schema, to conforming to the new schema.

        This migrator uses partial migrators. It runs them in the order in which they were designed to be run.
        """

        migrator_classes = get_migrators()
        num_migrators = len(migrator_classes)
        for idx, migrator_class in enumerate(migrator_classes):
            self.logger.info(f"Running migrator {idx + 1} of {num_migrators}")
            migrator = migrator_class(adapter=self.adapter, logger=self.logger)
            migrator.upgrade()
