from nmdc_schema.migrators.migrator_base import MigratorBase
import difflib

class Migrator(MigratorBase):
    """Migrates data from schema X to PR23"""

    _from_version = "X"
    _to_version = "PR23"

    def __init__(self, *args, **kwargs) -> None:
        """Invokes parent constructor and populates collection-to-transformations map."""

        super().__init__(*args, **kwargs)

        # Populate the "collection-to-transformers" map for this specific migration.
        self._agenda = dict(
            metagenome_assembly_set=[self.standardize_execution_resource], 
            metagenome_annotation_activity_set=[self.standardize_execution_resource],
            metatranscriptome_activity_set=[self.standardize_execution_resource], 
            mags_activity_set=[self.standardize_execution_resource],
            metagenome_sequencing_activity_set=[self.standardize_execution_resource], 
            read_qc_analysis_activity_set=[self.standardize_execution_resource],
            read_based_taxonomy_analysis_activity_set=[self.standardize_execution_resource], 
            metabolomics_analysis_activity_set=[self.standardize_execution_resource],
            metaproteomics_analysis_activity_set=[self.standardize_execution_resource], 
            nom_analysis_activity_set=[self.standardize_execution_resource]
        )

    def standardize_execution_resource(self, workflow_execution: dict):
        r"""
        Transforms the values of the execution_resource slot for any subclasses of WorkflowExecutionActivity into the
        allowable permissible values of the ExecutionResourceEnum.
        
        >>> m = Migrator()
        >>> m.standardize_execution_resource({'id': 123, 'execution_resource': 'LANL B-div'})
        {'id': 123, 'execution_resource': 'LANL-B-div'}
        >>> m.standardize_execution_resource({'id': 234, 'execution_resource': 'NERSC - Cori'})
        {'id': 234, 'execution_resource': 'NERSC-Cori'}
        """

        workflow_id = workflow_execution["id"]

        # allowable permissible values
        allowed_execution_resources = ['NERSC-Cori', 'NERSC-Perlmutter', 'EMSL', 'EMSL-RZR', 'JGI', 'LANL-B-div']
        
        if 'execution_resource' in workflow_execution:
            
            workflow_resource_value = workflow_execution['execution_resource']

            # Get the permissible value, if any, that is most similar to the original value
            # and has a similarity score of at least 0.8 with respect to the original value.
            # Reference: https://docs.python.org/3/library/difflib.html#difflib.get_close_matches
            matches = difflib.get_close_matches(workflow_resource_value, allowed_execution_resources, n=1, cutoff=0.8)
            
            if matches:

                if workflow_resource_value != matches[0]:
                    # change value of the workflow_execution resource to the proper permissible value if the match is not 100%
                    self.logger.info(f"Changing the workflow {workflow_id} execution_resource value from {workflow_resource_value} to {matches[0]}")
                    workflow_execution['execution_resource'] = matches[0]

            else:
                self.logger.error(f"The workflow {workflow_id} has an execution_resource value of {workflow_resource_value}, but did not have any matches with the cutoff set at 0.8")

        return workflow_execution

    