from typing import Dict, Set, Union
from datetime import datetime

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

    # Mapping from `workflow_chain_set` document `id` to its sets of `has_input` and `has_output` values.
    # Example: {'wfc-id-april': {'inputs': set('wfc-id-january', ...), 'outputs': set('wfc-id-february', ...)}}
    id_to_inputs_and_outputs_map: Dict[str, Dict[str, Set[str]]] = {}

    # Mapping from `workflow_chain_set` document `id` to the latest `ended_at_time` among all of the
    # `workflow_execution_set` documents that claim to be `part_of` that `WorkflowExecution`.
    id_to_workflow_execution_ended_at_times_map: Dict[str, datetime] = {}

    # Mapping from `workflow_execution_set` document `id` to the `id`s of the `workflow_chain_set` documents
    # that the former is a `part_of`, and to the `ended_at_time` of the former.
    workflow_execution_id_to_wfc_ids_and_ended_at_time_map: Dict[
        str, Dict[str, Union[Set[str], datetime]]
    ] = {}

    # A mapping from `workflow_chain_set` document `id` to its eventual `replaces` value, if any.
    # Example: {'wfc-id-april': 'wfc-id-january', 'wfc-id-march': 'wfc-id-february', ...}
    id_to_replaces_map: Dict[str, str] = {}

    def upgrade(self) -> None:
        r"""
        Migrates the database from conforming to the original schema, to conforming to the new schema.
        """

        # Determine the values we will later write to the documents.
        self.adapter.do_for_each_document(
            collection_name="workflow_chain_set",
            action=self.collect_input_and_output_values,
        )

        self.adapter.do_for_each_document(
            collection_name="workflow_execution_set",
            action=self.collect_workflow_chain_ids_and_ended_at_times,
        )

        # Write the values to the documents.
        self.adapter.process_each_document(
            collection_name="workflow_chain_set",
            pipeline=[self.write_the_replaces_value],
        )

    def collect_workflow_chain_ids_and_ended_at_times(
        self, workflow_execution: dict
    ) -> None:
        r"""
        Compiles a mapping from `id` values of `workflow_execution_set` documents, to `id` values of
        the `workflow_chain_set` documents that the former are a `part_of`; and to the `ended_at_time` value
        of the former, represented as a Python `datetime` instance.

        >>> m = Migrator()
        >>> len(m.workflow_execution_id_to_wfc_ids_and_ended_at_time_map.items())
        0
        >>> m.collect_workflow_chain_ids_and_ended_at_times({'id': 'wfe1',
        ...                                                  'part_of': ['wfc1', 'wfc2'],
        ...                                                  'ended_at_time': '2024-01-01T09:30:00+00:00'})
        >>> len(m.workflow_execution_id_to_wfc_ids_and_ended_at_time_map.items())
        1
        >>> 'wfe1' in m.workflow_execution_id_to_wfc_ids_and_ended_at_time_map.keys()
        True
        >>> wfc_ids = m.workflow_execution_id_to_wfc_ids_and_ended_at_time_map['wfe1']['workflow_chain_ids']
        >>> ts = m.workflow_execution_id_to_wfc_ids_and_ended_at_time_map['wfe1']['ended_at_datetime']
        >>> 'wfc1' in wfc_ids
        True
        >>> 'wfc2' in wfc_ids
        True
        >>> # References:
        >>> # - https://docs.python.org/3/library/datetime.html#datetime.datetime.timestamp
        >>> # - https://www.timestamp-converter.com/
        >>> type(ts) is datetime
        True
        >>> ts.timestamp()
        1704101400.0
        """

        workflow_execution_id = workflow_execution["id"]
        workflow_chain_ids = workflow_execution["part_of"]
        ended_at_time: str = workflow_execution["ended_at_time"]
        ended_at_datetime = datetime.fromisoformat(ended_at_time)  # parses it as an ISO 8601 string
        self.workflow_execution_id_to_wfc_ids_and_ended_at_time_map[
            workflow_execution_id
        ] = dict(
            workflow_chain_ids=set(workflow_chain_ids),
            ended_at_datetime=ended_at_datetime,
        )

    def collect_input_and_output_values(self, workflow_chain: dict) -> None:
        r"""
        Compiles a mapping from `id` values to sets of `has_input` and `has_output` values.

        >>> m = Migrator()
        >>> len(m.id_to_inputs_and_outputs_map.items())
        0
        >>> m.collect_input_and_output_values({'id': 'wfc1', 'has_input': ['i1'], 'has_output': ['o1']})
        >>> len(m.id_to_inputs_and_outputs_map.items())
        1
        >>> m.id_to_inputs_and_outputs_map['wfc1']['inputs']
        {'i1'}
        >>> m.id_to_inputs_and_outputs_map['wfc1']['outputs']
        {'o1'}
        >>> m.collect_input_and_output_values({'id': 'wfc2', 'has_input': ['i1'], 'has_output': ['o1', 'o2']})
        >>> len(m.id_to_inputs_and_outputs_map.items())
        2
        >>> m.id_to_inputs_and_outputs_map['wfc2']['inputs']
        {'i1'}
        >>> 'o1' in m.id_to_inputs_and_outputs_map['wfc2']['outputs']
        True
        >>> 'o2' in m.id_to_inputs_and_outputs_map['wfc2']['outputs']
        True
        """

        workflow_chain_id = workflow_chain["id"]
        inputs = workflow_chain["has_input"] if "has_input" in workflow_chain else []
        outputs = workflow_chain["has_output"] if "has_output" in workflow_chain else []
        self.id_to_inputs_and_outputs_map[workflow_chain_id] = dict(
            inputs=set(inputs),
            outputs=set(outputs),
        )

    def has_same_inputs_and_different_outputs(
        self, wfc_id_a: str, wfc_id_b: str
    ) -> bool:
        r"""
        Checks whether the two `WorkflowChain` documents having the specified `id` values,
        have the same `has_input` values while having different `has_output` values.

        >>> m = Migrator()
        >>> m.id_to_inputs_and_outputs_map = {'wfc1': {'inputs': {'i1'}, 'outputs': {'o1'}},  # original
        ...                                   'wfc2': {'inputs': {'i1'}, 'outputs': {'o1'}},  # same ins/outs
        ...                                   'wfc3': {'inputs': {'i1'}, 'outputs': {'o2'}},  # same ins only
        ...                                   'wfc4': {'inputs': {'i2'}, 'outputs': {'o1'}},  # same outs only
        ...                                   'wfc5': {'inputs': {'i2'}, 'outputs': {'o2'}}}  # different ins/outs
        >>> m.has_same_inputs_and_different_outputs('wfc1', 'wfc2')
        False
        >>> m.has_same_inputs_and_different_outputs('wfc1', 'wfc3')
        True
        >>> m.has_same_inputs_and_different_outputs('wfc1', 'wfc4')
        False
        >>> m.has_same_inputs_and_different_outputs('wfc1', 'wfc5')
        False
        >>> m.id_to_inputs_and_outputs_map = {'wfc11': {'inputs': {'i1', 'i2'}, 'outputs': {'o1', 'o2'}},  # original
        ...                                   'wfc12': {'inputs': {'i2', 'i1'}, 'outputs': {'o2', 'o1'}},  # re-ordered
        ...                                   'wfc13': {'inputs': {'i2', 'i1'}, 'outputs': {'o2', 'o1', 'o3'}}}  # more
        >>> m.has_same_inputs_and_different_outputs('wfc11', 'wfc12')
        False
        >>> m.has_same_inputs_and_different_outputs('wfc11', 'wfc13')
        True
        """

        wfc_a_inputs: Set[str] = self.id_to_inputs_and_outputs_map[wfc_id_a]["inputs"]
        wfc_b_inputs: Set[str] = self.id_to_inputs_and_outputs_map[wfc_id_b]["inputs"]
        wfc_a_outputs: Set[str] = self.id_to_inputs_and_outputs_map[wfc_id_a]["outputs"]
        wfc_b_outputs: Set[str] = self.id_to_inputs_and_outputs_map[wfc_id_b]["outputs"]
        return wfc_a_inputs == wfc_b_inputs and wfc_a_outputs != wfc_b_outputs

    def determine_the_replaces_value(
        self, workflow_chain_id: str, id_to_inputs_and_outputs_map: dict
    ) -> None:
        raise NotImplementedError  # TODO

    def write_the_replaces_value(self, workflow_chain: dict) -> dict:
        raise NotImplementedError  # TODO
