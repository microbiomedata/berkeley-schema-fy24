from nmdc_schema.migrators.migrator_base import MigratorBase

class Migrator_from_X_to_pr2_and_pr24(MigratorBase):
    """Migrates data from schema X to PR2 and PR24"""

    def __init__(self, *args, **kwargs) -> None:
        """Invokes parent constructor and populates collection-to-transformations map."""

        super().__init__(*args, **kwargs)

        # Populate the "collection-to-transformers" map for this specific migration.
        self.agenda = [
            self.change_class_names,
        ]

    def change_class_names(self, database: dict):
        r"""
        Transforms class/collection names into a new desired name"
        
        >>> m = Migrator_from_X_to_pr2_and_pr24()
        >>> m.change_class_names({'mags_activity_set': {'id': 123, 'key': 'value'}, 'metabolomics_analysis_activity_set': {'id': 234,
        ...     'key': 'value'}, 'metagenome_annotation_activity_set': {'id': 345, 'key': 'value'}, 'metagenome_sequencing_activity_set': {
        ...     'id': 456, 'key': 'value'}, 'metaproteomics_analysis_activity_set': {'id': 567, 'key': 'value'}, 
        ...     'metatranscriptome_activity_set': {'id': 678, 'key': 'value'}, 'nom_analysis_activity_set': {'id': 891, 'key': 'value'},
        ...     'read_based_taxonomy_analysis_activity_set': {'id': 457, 'key': 'value'}, 'read_qc_analysis_activity_set': {'id': 764, 
        ...     'key': 'value'}, 'omics_processing_set': {'id': 935, 'key': 'value'}})
        {'mags_set': {'id': 123, 'key': 'value'}, 'metabolomics_analysis_set': {'id': 234, 'key': 'value'}, 'metagenome_annotation_set': {'id': 345, 'key': 'value'}, 'metagenome_sequencing_set': {'id': 456, 'key': 'value'}, 'metaproteomics_analysis_set': {'id': 567, 'key': 'value'}, 'metatranscriptome_analysis_set': {'id': 678, 'key': 'value'}, 'nom_analysis_set': {'id': 891, 'key': 'value'}, 'read_based_taxonomy_analysis_set': {'id': 457, 'key': 'value'}, 'read_qc_analysis_set': {'id': 764, 'key': 'value'}, 'data_generation_set': {'id': 935, 'key': 'value'}}
        """

        collection_names_to_change = {
            "mags_activity_set": "mags_set",
            "metabolomics_analysis_activity_set": "metabolomics_analysis_set",
            "metagenome_annotation_activity_set": "metagenome_annotation_set",
            "metagenome_sequencing_activity_set": "metagenome_sequencing_set",
            "metaproteomics_analysis_activity_set": "metaproteomics_analysis_set",
            "metatranscriptome_activity_set": "metatranscriptome_analysis_set",
            "nom_analysis_activity_set": "nom_analysis_set",
            "read_based_taxonomy_analysis_activity_set": "read_based_taxonomy_analysis_set",
            "read_qc_analysis_activity_set": "read_qc_analysis_set",
            "omics_processing_set": "data_generation_set"
            }
         
        for k, v in collection_names_to_change.items():
            database[v] = database.pop(k)
        
        return database

    