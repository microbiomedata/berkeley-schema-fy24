"""Data test."""
import os
import pprint
import unittest

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import OrderedBy
from linkml_runtime.linkml_model.meta import ClassDefinition

ROOT = os.path.join(os.path.dirname(__file__), '..')
SCHEMA_DIR = os.path.join(ROOT, "src", "schema")

SCHEMA_FILE = os.path.join(SCHEMA_DIR, 'nmdc.yaml')

allowed_typeless_classes = set()

allowed_typeless_classes.add('Database')


class TestAllMultivaluedClassRangeSlotsAreInlinedAsList(unittest.TestCase):
    """Test data and datamodel."""

    def test_all_multivalued_class_range_slots_are_inlined_as_list(self):
        view = SchemaView(SCHEMA_FILE)
        print("\n")

        all_class_names = list(view.all_classes(ordered_by=OrderedBy.LEXICAL).keys())

        all_class_names.sort()

        for current_class in all_class_names:
            current_induced_class = view.induced_class(current_class)
            current_induced_slots = current_induced_class.attributes

            for sk, sv in sorted(current_induced_slots.items()):
                # print(f"{current_class} {sk}")
                # print(f"{sv.range = }")
                # print(f"{sv.multivalued = }")
                #
                # x = view.get_element(sv.range)
                # print(type(x))

                if isinstance(view.get_element(sv.range), ClassDefinition) and sv.multivalued:
                    # check if the class in the range has an identifiers slot
                    range_identifier = view.get_identifier_slot(sv.range)
                    # print(f"{range_identifier = }")
                    if range_identifier is not None:
                        # print(f"{current_class} {sk} {sv.range} {range_identifier}")
                        pass
                    else:
                        # self.assertTrue(sv.inlined_as_list, msg=f"{current_class} {sk} is not inlined_as_list")
                        print(f"{current_class}.{sk}")  # is not inlined_as_list
