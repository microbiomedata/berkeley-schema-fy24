import os
import pprint

import yaml


def read_yaml_files(directory):
    yaml_data = []

    file_list = list(os.listdir(directory))
    file_list.sort()

    # Iterate over all files in the directory
    for filename in file_list:
        print(filename)
        # Check if the file has a .yaml or .yml extension
        if filename.endswith(('.yaml', '.yml')):
            file_path = os.path.join(directory, filename)

            # Open the file and parse the YAML content
            with open(file_path, 'r') as file:
                try:
                    data = yaml.safe_load(file)
                    yaml_data.append(data)
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML file {filename}: {e}")

    return yaml_data


lod = read_yaml_files('../schema/')

class_definitions = {}
enum_definitions = {}
range_usages = {}
slot_definitions = {}
# slot_usages = {}
for module in lod:
    mod_id = str(module['id'])
    if 'classes' in module and module['classes'] is not None:
        for ck, cv in module['classes'].items():
            class_name = str(ck)
            class_definitions[class_name] = mod_id
    if 'slots' in module and module['slots'] is not None:
        for sk, sv in module['slots'].items():
            slot_name = str(sk)
            slot_definitions[slot_name] = mod_id
            if isinstance(sv, dict):
                if 'range' in sv:
                    range_name = sv['range']
                    range_usages[range_name] = mod_id
                else:
                    print(f"{slot_name} does not have a range")
            else:
                print(f"{slot_name} is not a dict")
            # if 'range' in sv and sv['range'] is not None:
            #     print(sv['range'])
    if 'enums' in module and module['enums'] is not None:
        for ek, ev in module['enums'].items():
            enums_name = str(ek)
            enum_definitions[enums_name] = mod_id

final_dict = {
    'class_definitions': class_definitions,
    'enum_definitions': enum_definitions,
    'slot_definitions': slot_definitions,
    'range_usages': range_usages
}

with open('../../assets/usage_files_vs_definition_files.yaml', 'w') as file:
    yaml.dump(final_dict, file)
