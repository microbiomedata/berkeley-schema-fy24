from nmdc_schema.migrators.migrator_base import MigratorBase


class Migrator(MigratorBase):
    r"""
    Migrates a database between two schemas.

    This migrator adds a field named `replaces` to each document in the `workflow_chain_set` collection
    that has a predecessor. The value of the field is the `id` of that predecessor.

    Note: This migrator was designed to accommodate the schema changes introduced in PR193:
          https://github.com/microbiomedata/berkeley-schema-fy24/pull/193

    Note: This migrator was designed to be run at some time after (a) the migrator that creates and populates the
          `workflow_chain_set` collection has been run (that migrator is implemented in `./migrator_from_X_to_PR9.py`);
          and (b) the migrator that consolidates the `PlannedProcess` grandchild collections into the `PlannedProcess`
          immediate child collections (that migrator is implemented in `./migrator_from_PR104_to_PR195.py`).
    """

    _from_version = "X"
    _to_version = "PR193"

    # A mapping from `workflow_chain_set` document `id` to its eventual `replaces` value, if any.
    # Example: {'wfc-id-april': 'wfc-id-january', 'wfc-id-march': 'wfc-id-february', ...}
    id_to_replaces_map = dict()

    def upgrade(self) -> None:
        r"""
        Migrates the database from conforming to the original schema, to conforming to the new schema.
        """

        # Determine the values we will later write to the documents.
        self.adapter.do_for_each_document(
            collection_name="workflow_chain_set",
            action=self.compile_replaces_values,
        )

        # Write the values to the documents.
        self.adapter.process_each_document(
            collection_name="workflow_chain_set",
            pipeline=[self.set_replaces_field],
        )

    def compile_replaces_values(self, workflow_chain: dict) -> None:
        raise NotImplementedError  # TODO

    def set_replaces_field(self, workflow_chain: dict) -> dict:
        raise NotImplementedError  # TODO
