from typing import Dict, List
from logging import getLogger
from nmdc_schema.migrators.adapters.adapter_base import AdapterBase


class MigratorBase:
    """Base class containing properties and methods related to migrating data between two schema versions."""

    # The schema version from which this class migrates data.
    #
    # Note: This string is empty here. It will be populated within the migration-specific classes.
    #
    _from_version: str = ""

    # The schema version to which this class migrates data.
    #
    # Note: This string is empty here. It will be populated within the migration-specific classes.
    #
    _to_version: str = ""

    def __init__(self, adapter: AdapterBase = None, logger=None):
        # Store a reference to the specified adapter instance. The adapter instance will be used to perform
        # database operations beyond the original one-document-at-a-time, self-contained transformations;
        # for example, renaming collections and creating documents based upon values in other documents.
        self.adapter = adapter

        # If a logger was specified, use it; otherwise, initialize one and use that.
        self.logger = getLogger(__name__) if logger is None else logger

        if self.adapter is None:
            self.logger.warning("No adapter was specified. Migration capability will be limited.")

        # Define the "agenda" of transformations that constitute this migration.
        #
        # Note: This is a dictionary that maps a given collection to a list of "transformation" functions.
        #       Each key is a collection name, and each value is a list. Each element of the list is a
        #       so-called "transformation" function. A "transformation" function is a function that
        #       transforms something from one schema version to another. In this case, the "something"
        #       is a dictionary representing a single document from the specified collection.
        #
        # Note: This dictionary is empty here. It will be populated within the "constructor" functions
        #       of the migration-specific classes (i.e. the classes that inherit from this base class).
        #
        self._agenda: Dict[str, List[callable]] = dict()

    @classmethod
    def get_origin_version(cls) -> str:
        """Returns the schema version this class migrates data from."""
        return cls._from_version

    @classmethod
    def get_destination_version(cls) -> str:
        """Returns the schema version this class migrates data to."""
        return cls._to_version

    def get_transformers_for(self, collection_name: str) -> List[callable]:
        """Returns the list of transformers defined for the specified collection."""
        return self._agenda.get(collection_name, [])
