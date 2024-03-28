import pprint

import linkml_runtime
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import OrderedBy

schema_file = '../schema/nmdc.yaml'

schema_view = SchemaView(schema_file)

schema_slots = schema_view.all_slots(ordered_by=OrderedBy.LEXICAL)

for sk, sv in schema_slots.items():
    classes_for_slot = schema_view.get_classes_by_slot(sv)
    if len(classes_for_slot) == 0:
        slot_uri_suffix = f", {sv.slot_uri}" if sv.slot_uri else ""
        slot_children = schema_view.slot_children(sk)
        slot_children_prefix = f"parent " if len(slot_children) > 0 else ""
        print(f"No classes for {slot_children_prefix}slot {sk}{slot_uri_suffix}")

schema_enums = schema_view.all_enums()
for ek, ev in schema_enums.items():
    slots_for_enim = schema_view.get_slots_by_enum(ek)
    if len(slots_for_enim) == 0:
        print(f"No slots for {ek}")

schema_types = schema_view.all_types()
pprint.pprint(list(schema_types.keys()))

schema_elements = schema_view.all_elements()

whitespace_keys = [key for key in schema_elements.keys() if any(char.isspace() for char in key)]

for wsk in whitespace_keys:
    wse = schema_view.get_element(wsk)

    if type(wse) is linkml_runtime.linkml_model.meta.EnumDefinition:
        wse.permissible_values = None

    if wse.from_schema != "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/mixs.yaml":
        print(yaml_dumper.dumps(wse))
