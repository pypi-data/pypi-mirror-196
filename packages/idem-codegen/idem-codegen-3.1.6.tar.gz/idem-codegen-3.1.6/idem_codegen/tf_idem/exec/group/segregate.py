import json
import os
from collections import ChainMap
from collections import OrderedDict

import inflection as inflection
import yaml


def generate_sls_files_for_tf_files_in_dir(
    hub, dir_path, count, output_dir_path, run_name, git_dict
):
    filtered_sls_data = hub.tf_idem.RUNS["SLS_DATA"]
    tf_resource_type__name_to_tf_resource_map = hub.tf_idem.RUNS["TF_IDEM_RESOURCE_MAP"]
    tfvars_data = hub.tf_idem.RUNS["TF_VARS"]

    if git_dict:
        module_output_directory_path = output_dir_path
    else:
        module_output_directory_path = os.path.join(
            output_dir_path,
            os.sep.join(dir_path.split(os.sep)[count:]),
        )
    complete_resource_map = {}
    complete_tf_resource_map = {}
    complete_dict_of_variables = {}
    name_of_files_in_module = set()
    if git_dict:
        (
            resource_map,
            idem_resource_id_tf_resource_map,
            variables,
        ) = convert_tf_file_to_sls(
            hub,
            dir_path,
            filtered_sls_data,
            tfvars_data,
            tf_resource_type__name_to_tf_resource_map,
            module_output_directory_path,
            git_dict,
            output_dir_path,
            run_name,
        )
        if resource_map is not None:
            complete_resource_map.update(resource_map)
        if idem_resource_id_tf_resource_map is not None:
            complete_tf_resource_map.update(idem_resource_id_tf_resource_map)
        if variables is not None:
            complete_dict_of_variables.update(variables)
        git_dict["name_of_files_in_module"].add(
            f"sls.{(dir_path[dir_path.rfind('/') + 1:])[:-3]}"
        )
    else:
        for file in os.listdir(dir_path):
            if not file.endswith(".tf"):
                continue
            tf_file_path = os.path.join(dir_path, file)
            (
                resource_map,
                idem_resource_id_tf_resource_map,
                variables,
            ) = convert_tf_file_to_sls(
                hub,
                tf_file_path,
                filtered_sls_data,
                tfvars_data,
                tf_resource_type__name_to_tf_resource_map,
                module_output_directory_path,
                None,
                output_dir_path,
                run_name,
            )
            if resource_map is not None:
                complete_resource_map.update(resource_map)
            if idem_resource_id_tf_resource_map is not None:
                complete_tf_resource_map.update(idem_resource_id_tf_resource_map)
            if variables is not None:
                complete_dict_of_variables.update(variables)
            name_of_files_in_module.add(f"sls.{file[:-3]}")

    hub.tf_idem.RUNS["ALL_SLS_RESOURCES"] = complete_resource_map
    if hub.tf_idem.RUNS.get("TF_RESOURCE_MAP"):
        hub.tf_idem.RUNS["TF_RESOURCE_MAP"].update(complete_tf_resource_map)
    else:
        hub.tf_idem.RUNS["TF_RESOURCE_MAP"] = complete_tf_resource_map

    if "TF_VARIABLES" not in hub.tf_idem.RUNS:
        hub.tf_idem.RUNS["TF_VARIABLES"] = {}
    # Change values of bool type into string type
    complete_dict_of_variables = hub.tf_idem.tool.utils.change_bool_values_to_string(
        complete_dict_of_variables
    )
    hub.tf_idem.RUNS["TF_VARIABLES"].update(complete_dict_of_variables)

    if git_dict:
        name_of_files_in_module = git_dict["name_of_files_in_module"].copy()
    # Generate parent init file
    os.makedirs(
        os.path.dirname(f"{module_output_directory_path}/init.sls"),
        exist_ok=True,
    )
    files_to_exclude_in_parent_init = {"sls.variables"}
    with open(f"{module_output_directory_path}/init.sls", "w") as _file:
        yaml.dump(
            {
                "include": sorted(
                    list(
                        name_of_files_in_module.difference(
                            files_to_exclude_in_parent_init
                        )
                    )
                )
            },
            _file,
            default_flow_style=False,
        )

    # Generate variables.sls file to contain all the variables used in the module
    os.makedirs(
        os.path.dirname(f"{module_output_directory_path}/params/variables.sls"),
        exist_ok=True,
    )
    with open(f"{module_output_directory_path}/params/variables.sls", "w") as file1:
        yaml.dump(complete_dict_of_variables, file1, default_flow_style=False)
    if not hub.idem_codegen.RUNS["COMMON_VARIABLES"]:
        hub.idem_codegen.RUNS["COMMON_VARIABLES"] = complete_dict_of_variables
    else:
        hub.idem_codegen.RUNS["COMMON_VARIABLES"] = {
            x: hub.idem_codegen.RUNS["COMMON_VARIABLES"][x]
            for x in hub.idem_codegen.RUNS["COMMON_VARIABLES"]
            if x in complete_dict_of_variables
        }


def convert_tf_file_to_sls(
    hub,
    tf_file_path,
    filtered_sls_data,
    tfvars_data,
    tf_resource_type__name_to_tf_resource_map,
    module_output_directory_path,
    git_dict,
    output_dir_path,
    run_name,
):
    hub.log.info("Converting : '%s'", tf_file_path)

    _, tf_file_name = os.path.split(tf_file_path)
    tf_file_data = hub.tf_idem.tool.utils.parse_tf_data(tf_file_path, git_dict)

    tf_idem_resource_type_map = hub.tf_idem.tool.utils.tf_idem_resource_type_map
    __seperator = hub.idem_codegen.tool.utils.separator

    converted_sls_data = OrderedDict()
    idem_resource_id_map = OrderedDict()
    security_group_ids = []
    bucket_names = []
    idem_resource_id_tf_resource_map = OrderedDict()

    # Process data sources
    data_sources = tf_file_data.get("data", {})
    for tf_data_source in data_sources:
        if (
            tf_idem_resource_type_map.get(
                inflection.singularize(list(tf_data_source.keys())[0])
            )
            is None
        ):
            hub.log.warning(
                "Skipping conversion : No identifier found for resource %s present in file %s",
                list(tf_data_source.keys())[0],
                tf_file_path,
            )
            continue
        data_source = convert_data_source(
            hub, tf_data_source, tf_idem_resource_type_map
        )
        converted_sls_data.update(data_source)
    # Process resources
    resources = tf_file_data.get("resource", {})
    for tf_resource in resources:
        tf_resource_type = list(tf_resource.keys())[0]
        tf_resource_name = list(tf_resource[tf_resource_type].keys())[0]

        tf_resource_identifier = f"{tf_resource_type}{__seperator}{tf_resource_name}"
        if tf_resource_identifier not in tf_resource_type__name_to_tf_resource_map:
            hub.log.warning(
                "Skipping conversion : No identifier found for resource %s present in file %s",
                tf_resource_name,
                tf_file_path,
            )
            continue

        tf_state_for_resource = tf_resource_type__name_to_tf_resource_map[
            tf_resource_identifier
        ]
        if not tf_state_for_resource:
            hub.log.warning(
                "Skipping conversion : No state found for resource %s present in file %s",
                tf_resource_name,
                tf_file_path,
            )
            continue

        for instance in tf_state_for_resource["instances"]:
            attributes = instance["attributes"]
            if tf_resource_type == "aws_security_group":
                security_group_ids.append(attributes["id"])
            if tf_resource_type == "aws_s3_bucket":
                bucket_names.append(attributes["id"])

            # Get tf_uuid for this resource
            tf_uuid = (
                "id"
                if tf_resource_type not in hub.tf_idem.tool.utils.tf_resource_type_uuid
                else hub.tf_idem.tool.utils.tf_resource_type_uuid[tf_resource_type]
            )

            # Find equivalent SLS resource in 'filtered_sls_data' using tf_uuid
            sls_resource = None
            if (
                tf_uuid in attributes
                and f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{attributes[tf_uuid]}"
                in filtered_sls_data
            ):
                sls_resource = filtered_sls_data[
                    f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{attributes[tf_uuid]}"
                ]
            else:
                (
                    tf_unique_key_value_found_successfully,
                    tf_unique_value,
                    idem_unique_value,
                ) = hub.tf_idem.tool.utils.generate_tf_unique_value(
                    tf_uuid, attributes, tf_resource_type
                )
                if (
                    tf_unique_key_value_found_successfully
                    and f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{tf_unique_value}"
                    in filtered_sls_data
                ):
                    sls_resource = filtered_sls_data[
                        f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{tf_unique_value}"
                    ]

            if sls_resource:
                resource_path_to_update = sls_resource["resource_path"]
                converted_sls_data[resource_path_to_update] = sls_resource["resource"]
                idem_resource_id_tf_resource_map[
                    f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{sls_resource.get('idem_resource_id')}"
                ] = tf_resource
                idem_resource_attributes_map = dict(
                    ChainMap(*list(sls_resource["resource"].values())[0])
                )
                if "arn" in idem_resource_attributes_map:
                    idem_resource_id_map[
                        f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{idem_resource_attributes_map.get('arn')}"
                    ] = {
                        "resource": sls_resource["resource"],
                        "resource_path": resource_path_to_update,
                        "type": "arn",
                    }
                idem_resource_id_map[
                    f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{sls_resource.get('idem_resource_id')}"
                ] = {
                    "resource": sls_resource["resource"],
                    "resource_path": resource_path_to_update,
                    "type": "resource_id",
                }
                converted_sls_data.update({})

        if security_group_ids:
            security_group_rule_index = 0
            for resource in filtered_sls_data.values():
                if "aws.ec2.security_group_rule.present" not in resource["resource"]:
                    continue
                resource_map = ChainMap(
                    *resource["resource"]["aws.ec2.security_group_rule.present"]
                )
                if resource_map.get("group_id") not in security_group_ids:
                    continue
                converted_sls_data[
                    resource_path_to_update + "-rule-" + str(security_group_rule_index)
                ] = resource["resource"]
                idem_resource_id_map[
                    f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{resource['idem_resource_id']}"
                ] = {
                    "resource": resource["resource"],
                    "resource_path": resource_path_to_update
                    + "-rule-"
                    + str(security_group_rule_index),
                    "type": "resource_id",
                }
                security_group_rule_index = security_group_rule_index + 1

        if bucket_names:
            s3_bucket_names_index = 0
            for resource in filtered_sls_data.values():
                if "aws.s3.bucket_encryption.present" in resource["resource"]:
                    resource_map = ChainMap(
                        *resource["resource"]["aws.s3.bucket_encryption.present"]
                    )
                    if resource_map.get("resource_id") in bucket_names:

                        res_path = resource_path_to_update
                        res_path = res_path.replace(".", "_encryption.")
                        converted_sls_data[
                            res_path + "-" + str(s3_bucket_names_index)
                        ] = resource["resource"]
                        idem_resource_id_map[
                            f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{resource['idem_resource_id']}"
                        ] = {
                            "resource": resource["resource"],
                            "resource_path": res_path
                            + "-"
                            + str(s3_bucket_names_index),
                            "type": "resource_id",
                        }
                        s3_bucket_names_index = s3_bucket_names_index + 1

                if "aws.s3.bucket_lifecycle.present" in resource["resource"]:
                    resource_map = ChainMap(
                        *resource["resource"]["aws.s3.bucket_lifecycle.present"]
                    )
                    if resource_map.get("resource_id") in bucket_names:

                        res_path = resource_path_to_update
                        res_path = res_path.replace(".", "_lifecycle.")
                        converted_sls_data[
                            res_path + "-" + str(s3_bucket_names_index)
                        ] = resource["resource"]
                        idem_resource_id_map[
                            f"{tf_idem_resource_type_map.get(tf_resource_type)}{__seperator}{resource['idem_resource_id']}"
                        ] = {
                            "resource": resource["resource"],
                            "resource_path": res_path
                            + "-"
                            + str(s3_bucket_names_index),
                            "type": "resource_id",
                        }
                        s3_bucket_names_index = s3_bucket_names_index + 1

    if "variables.tf" != tf_file_name:
        output_sls_file_path = (
            f"{module_output_directory_path}/sls/{tf_file_name.replace('.tf', '')}"
        )
        os.makedirs(os.path.dirname(output_sls_file_path), exist_ok=True)

        # Do not dump immediately. store it in the hub for later use. dump once remaining phases are done.
        # with open(output_sls_file_path, "w") as file:
        #     yaml.dump(
        #         dict(converted_sls_data),
        #         file,
        #         default_flow_style=False,
        #         Dumper=MyDumper,
        #     )
        hub[run_name].RUNS["SLS_DATA_GROUPED"][
            output_sls_file_path
        ] = converted_sls_data

    # Process variables
    variables = OrderedDict()
    if "variable" in tf_file_data:
        variables.update(
            convert_variables_tf_to_sls(tf_file_data.get("variable"), tfvars_data)
        )

    # Process output variables
    output_variables = OrderedDict()
    module_variables_map = hub.tf_idem.RUNS["MODULE_VARIABLES"]
    if "output" in tf_file_data:
        output_vars = tf_file_data.get("output")
        for var in output_vars:
            var_name = list(var.keys())[0]
            if var_name in module_variables_map:
                key = module_variables_map[var_name]
                output_variables[key] = var[var_name].get("value")

    if "OUTPUT_VARIABLES" not in hub.tf_idem.RUNS:
        hub.tf_idem.RUNS["OUTPUT_VARIABLES"] = {}

    hub.tf_idem.RUNS["OUTPUT_VARIABLES"].update(output_variables)

    # Process local entities
    local_variables = tf_file_data.get("locals", [])
    for local in local_variables:
        for key, value in local.items():
            variables.update({f"local_{key}": value})

    # Perform tf to sls conversion for each module present in the tf file
    for module in tf_file_data.get("module", {}):
        git_dict = {}

        module_name = list(module.keys())[0]
        if "git::git@gitlab" in module.get(module_name).get("source"):
            # assuming there will be only files to process and not directories or sub-directories.
            (
                git_dict["tf_files"],
                git_dict["git_file_path"],
                git_dict["project"],
            ) = hub.tf_idem.tool.utils.fetch_gitlab_tf_files(
                module.get(module_name).get("source"),
                hub.OPT.idem_codegen.private_token,
                hub.OPT.idem_codegen.gitlab_link,
                hub.OPT.idem_codegen.project_branch,
            )
            output_dir_path = os.path.join(
                output_dir_path,
                git_dict["git_file_path"][git_dict["git_file_path"].rfind("/") + 1 :],
            )
            git_dict["name_of_files_in_module"] = set()
            for tf_file in git_dict["tf_files"]:
                if not tf_file["name"].endswith(".tf"):
                    continue
                filepath = git_dict["git_file_path"] + "/" + tf_file["name"]
                count = filepath.count("/")
                hub.tf_idem.exec.group.segregate.generate_sls_files_for_tf_files_in_dir(
                    filepath, count, output_dir_path, run_name, git_dict
                )
        else:
            absolute_path_of_module_source = os.path.abspath(
                module.get(module_name).get("source")
            )
            count = absolute_path_of_module_source.count("/")
            for root, _, _ in os.walk(absolute_path_of_module_source):
                hub.tf_idem.exec.group.segregate.generate_sls_files_for_tf_files_in_dir(
                    root, count, output_dir_path, run_name, None
                )
    return idem_resource_id_map, idem_resource_id_tf_resource_map, variables


def convert_variables_tf_to_sls(variables, tfvars_data):
    sls_vars = dict()
    for variable in variables:
        for key, value in variable.items():
            if key in tfvars_data:
                sls_vars[key] = tfvars_data.get(key)
                continue
            type = value.get("type")
            val = value.get("default")
            if type:
                if "list" in type:
                    new_val = json.dumps(value.get("default"))
                else:
                    new_val = val if val is not None else ""
            else:
                new_val = val if val is not None else ""
            sls_vars[key] = new_val

    return sls_vars


def convert_data_source(hub, tf_data_source, tf_idem_resource_type_map):
    sls = {}
    tf_data_source_type = list(tf_data_source.keys())[0]
    data_source_name = list(list(tf_data_source.values())[0].keys())[0]
    data_body = list(list(tf_data_source.values())[0].values())[0]
    actual_data_resource_type = tf_idem_resource_type_map.get(
        inflection.singularize(tf_data_source_type)
    )

    data_source_label_sls = f"data.{tf_data_source_type}.{data_source_name}"

    kwargs = {}
    tags = {}
    for key, value in data_body.items():
        if key == "tags":
            for tag_key, tag_value in value.items():
                tags[tag_key] = tag_value
        elif key == "filter":
            for item in value:
                if item.get("name").startswith("tag:"):
                    tags[item.get("name")[len("tag:") :]] = item.get("values")
                else:
                    kwargs[item.get("name")] = item.get("values")
        else:
            kwargs[key] = value

    # convert filter
    if tf_data_source_type != inflection.singularize(tf_data_source_type):
        path = actual_data_resource_type + ".list"
    else:
        path = actual_data_resource_type + ".get"

    if tags:
        kwargs["tags"] = tags

    sls[data_source_label_sls] = {
        "exec.run": [
            {"path": path},
            {"kwargs": kwargs},
        ]
    }
    return sls
