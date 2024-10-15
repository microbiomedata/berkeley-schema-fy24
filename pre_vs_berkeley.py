import pprint

from linkml_runtime import SchemaView

# from terminado.management import preexec_fn

pre_path = "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/refs/tags/v10.9.1/src/schema/nmdc.yaml"

berkeley_path = "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/refs/tags/v11.0.1/src/schema/nmdc.yaml"

pre_view = SchemaView(pre_path)

berkeley_view = SchemaView(berkeley_path)

pre_classes = pre_view.all_classes()
pre_class_names = list(pre_classes.keys())
print(len(pre_class_names))

berkeley_classes = berkeley_view.all_classes()
berkeley_class_names = list(berkeley_classes.keys())
print(len(berkeley_class_names))

pre_only = [c for c in pre_class_names if c not in berkeley_class_names]

berkeley_only = [c for c in berkeley_class_names if c not in pre_class_names]

pprint.pprint(pre_only)

pprint.pprint(berkeley_only)

pre_roots = pre_view.class_roots()
pre_roots.sort()
pprint.pprint(pre_roots)
print(len(pre_roots))

berkeley_roots = berkeley_view.class_roots()
berkeley_roots.sort()
pprint.pprint(berkeley_roots)
print(len(berkeley_roots))

pre_only = [c for c in pre_roots if c not in berkeley_roots]
pprint.pprint(pre_only)
print(len(pre_only))

berkeley_only = [c for c in berkeley_roots if c not in pre_roots]
pprint.pprint(berkeley_only)
print(len(berkeley_only))

####

pre_slots = pre_view.all_slots()
pre_slot_names = list(pre_slots.keys())
print(f"{len(pre_slot_names)}")

berkeley_slots = berkeley_view.all_slots()
berkeley_slot_names = list(berkeley_slots.keys())
print(f"{len(berkeley_slot_names)}")

pre_only = [s for s in pre_slot_names if s not in berkeley_slot_names]
pre_only.sort()

berkeley_only = [s for s in berkeley_slot_names if s not in pre_slot_names]
berkeley_only.sort()

pprint.pprint(pre_only)
print(f"{len(pre_only)}")

pprint.pprint(berkeley_only)
print(f"{len(berkeley_only)}")
