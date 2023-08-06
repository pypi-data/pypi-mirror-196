import json
import os

import yaml

from idem_codegen.idem_codegen.tool.utils import MyDumperNoBlankLines
from idem_codegen.tf_idem.tool.utils import tf_resource_type_uuid


def read_json(path):
    _file = open(path)  # Open the json file
    json_data = json.loads(_file.read())  # Read the data from json file
    _file.close()
    return json_data


def get_idem_resource_id(hub, tf_instance, tf_resource_type):
    tf_attributes = (
        tf_instance["attributes_flat"]
        if "attributes_flat" in tf_instance
        else tf_instance["attributes"]
    )
    tf_uuid = (
        "id"
        if tf_resource_type not in tf_resource_type_uuid
        else tf_resource_type_uuid[tf_resource_type]
    )
    (
        tf_unique_key_value_found_successfully,
        tf_unique_value,
        idem_unique_value,
    ) = hub.tf_idem.tool.utils.generate_tf_unique_value(
        tf_uuid, tf_attributes, tf_resource_type
    )
    return (
        idem_unique_value
        if tf_unique_key_value_found_successfully
        else tf_attributes["id"]
    )


def get_idem_resource_suffix_val(hub, tf_instance, attribute_to_export):
    tf_attributes = (
        tf_instance["attributes_flat"]
        if "attributes_flat" in tf_instance
        else tf_instance["attributes"]
    )
    return (
        "." + tf_attributes[attribute_to_export]
        if attribute_to_export in tf_attributes
        else ""
    )


def init(hub):
    tf_state_file_path = hub.OPT.idem_codegen.tf_state_file_path
    output_file_path = hub.OPT.idem_codegen.output_directory_path
    tf_state_data = read_json(tf_state_file_path)
    resource_ids_map = {}
    resource_id_suffix = hub.OPT.idem_codegen.resource_id_suffix
    for tf_state_resource in tf_state_data["resources"]:
        count = 0
        if tf_state_resource.get("module"):
            module = tf_state_resource.get("module").replace("module.", "")
        else:
            # TODO: Add a better name instead of no-module.
            module = "no-module"
        tf_resource_type = tf_state_resource.get("type")
        if module not in resource_ids_map:
            resource_ids_map[module] = {}
        tf_instances = tf_state_resource.get("instances", [])

        for tf_instance in tf_instances:
            resource_id_value = (
                ""
                if tf_resource_type == "aws_security_group_rule"
                else get_idem_resource_id(hub, tf_instance, tf_resource_type)
            )
            resource_id_suffix_val = get_idem_resource_suffix_val(
                hub, tf_instance, resource_id_suffix
            )
            if len(tf_instances) > 1:
                resource_ids_map[module][
                    f"{tf_resource_type}.{tf_state_resource.get('name')}{resource_id_suffix_val}-{count}"
                ] = resource_id_value
            else:
                resource_ids_map[module][
                    f"{tf_resource_type}.{tf_state_resource.get('name')}{resource_id_suffix_val}"
                ] = resource_id_value
            count = count + 1

    for module, module_resource_map in resource_ids_map.items():
        output_file_name = os.path.join(
            output_file_path, "resource_ids_" + module + ".sls"
        )
        os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
        with open(output_file_name, "w") as file:
            file.truncate(0)
            yaml.dump(module_resource_map, file, Dumper=MyDumperNoBlankLines)
