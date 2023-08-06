import base64
import re

import gitlab
import hcl2

tf_resource_type_uuid_separator = {
    "aws_route53_zone_association": ":",
}

ternary_operator_pattern = re.compile(
    r"\${[\s\d\w. ]+\?[\s\d\w.[\] ]+:[\s\d\w.[\] ]+}|[\s\d\w. ]+\?[\s\d\w.[\] ]+:[\s\d\w.[\] ]+"
)

ternery_operator_pattern_in_jinja = re.compile(
    r'["$.{{\s\w\d()\[\]\/}}+\*|-]+\?["$.{{\s\w\d()\[\]\/}}+\*|-]+\:["$.{{\s\w\d()\[\]\/}}+\*|-]+'
)

var_pattern_unprocessed1 = r"\${var\.[\w.\[\]-]+"

var_pattern_unprocessed2 = r"var\.[\w.\[\]-]+"

count_index_pattern = r"\$[{ +\d]+count.index[ *\d-]+}"

params_variable_ends_with_count_pattern = r"\[.*\]$"

arg_reference_regex_pattern = re.compile(r"\${[^\${}]+}")

replace_pattern = re.compile(r"\${replace\([, _\\\n/\-\w.*\"-]+\)}")

# NOTE : For any new entry in this map, ensure to add required details in tf_resource_type_uuid,
# tf_resource_type_default_uuid, idem_resource_type_uuid and idem_resource_type_default_uuid
tf_idem_resource_type_map = {
    "aws_cloudwatch_log_group": "aws.cloudwatch.log_group",
    "aws_db_subnet_group": "aws.rds.db_subnet_group",
    "aws_eip": "aws.ec2.elastic_ip",
    "aws_elasticache_subnet_group": "aws.elasticache.cache_subnet_group",
    "aws_flow_log": "aws.ec2.flow_log",
    "aws_iam_role": "aws.iam.role",
    "aws_iam_role_policy": "aws.iam.role_policy",
    "aws_internet_gateway": "aws.ec2.internet_gateway",
    "aws_nat_gateway": "aws.ec2.nat_gateway",
    "aws_route_table": "aws.ec2.route_table",
    "aws_route_table_association": "aws.ec2.route_table_association",
    "aws_security_group": "aws.ec2.security_group",
    "aws_security_group_rule": "aws.ec2.security_group_rule",
    "aws_subnet": "aws.ec2.subnet",
    "aws_subnets": "aws.ec2.subnet",
    "aws_vpc": "aws.ec2.vpc",
    "aws_vpc_dhcp_options": "aws.ec2.dhcp_option",
    "aws_eks_cluster": "aws.eks.cluster",
    "aws_iam_policy": "aws.iam.policy",
    "aws_iam_role_policy_attachment": "aws.iam.role_policy_attachment",
    "aws_iam_user": "aws.iam.user",
    "aws_iam_user_policy": "aws.iam.user_policy",
    "aws_acm_certificate": "aws.acm.certificate_manager",
    "aws_launch_configuration": "aws.autoscaling.launch_configuration",
    "aws_cloudtrail": "aws.cloudtrail.trail",
    "aws_cloudwatch_metric_alarm": "aws.cloudwatch.metric_alarm",
    "aws_config_config_rule": "aws.config.rule",
    "aws_dynamodb_table": "aws.dynamodb.table",
    "aws_ami": "aws.ec2.ami",
    "aws_ecr_repository": "aws.ecr.repository",
    "aws_eks_addon": "aws.eks.addon",
    "aws_eks_node_group": "aws.eks.nodegroup",
    "aws_elasticache_parameter_group": "aws.elasticache.cache_parameter_group",
    "aws_iam_access_key": "aws.iam.access_key",
    "aws_iam_instance_profile": "aws.iam.instance_profile",
    "aws_iam_openid_connect_provider": "aws.iam.open_id_connect_provider",
    "aws_iam_user_policy_attachment": "aws.iam.user_policy_attachment",
    "aws_iam_user_ssh_key": "aws.iam.user_ssh_key",
    "aws_lambda_function": "aws.lambda_.function",
    "aws_route53_zone": "aws.route53.hosted_zone",
    "aws_route53_zone_association": "aws.route53.hosted_zone_association",
    "aws_s3_bucket": "aws.s3.bucket",
    "aws_s3_bucket_notification": "aws.s3.bucket_notification",
    "aws_s3_bucket_policy": "aws.s3.bucket_policy",
    "aws_sns_topic": "aws.sns.topic",
    "aws_sns_topic_policy": "aws.sns.topic_policy",
    "aws_sns_topic_subscription": "aws.sns.subscription",
    "aws_kms_key": "aws.kms.key",
    "aws_cloudwatch_event_rule": "aws.event.rule",
    "aws_ec2_transit_gateway": "aws.ec2.transit_gateway",
    "aws_rds_cluster": "aws.rds.db_cluster",
    "aws_rds_cluster_instance": "aws.rds.db_instance",
    "aws_route53_record": "aws.route53.resource_record",
    "aws_vpc_endpoint": "aws.ec2.vpc_endpoint",
    "aws_route_table_association": "aws.ec2.route_table_association",
    "aws_vpc_dhcp_options_association": "aws.ec2.dhcp_option_association",
    "aws_db_parameter_group": "aws.rds.db_parameter_group",
    "aws_instance": "aws.ec2.instance",
    "aws_kms_alias": "aws.kms.alias",
    "aws_rds_cluster_parameter_group": "aws.rds.db_cluster_parameter_group",
    "aws_s3_bucket_public_access_block": "aws.s3.public_access_block",
    "aws_efs_mount_target": "aws.efs.mount_target",
    "aws_eks_fargate_profile": "aws.eks.fargate_profile",
    "aws_efs_file_system": "aws.efs.file_system",
    "aws_autoscaling_group": "aws.autoscaling.auto_scaling_group",
    "aws_ec2_transit_gateway_vpc_attachment": "aws.ec2.transit_gateway_vpc_attachment",
    "aws_api_gateway_rest_api": "aws.apigateway.rest_api",
    "aws_api_gateway_integration": "aws.apigatewayv2.integration",
    "aws_lambda_permission": "aws.lambda_aws.function_permission",
    "aws_api_gateway_resource": "aws.apigateway.resource",
    "aws_cloudwatch_log_resource_policy": "aws.cloudwatchlogs.resource_policy",
    "aws_guardduty_detector": "aws.guardduty.detector",
    "aws_elasticache_replication_group": "aws.elasticache.replication_group",
    "aws_vpc_peering_connection": "aws.ec2.vpc_peering_connection",
    "aws_vpc_peering_connection_options": "aws.ec2.vpc_peering_connection_options",
    "aws_vpc_peering_connection_accepter": "aws.ec2.vpc_peering_acceptor",
    "aws_key_pair": "aws.ec2.key_pair",
    "aws_api_gateway_method": "aws.apigateway.method",
    "aws_acm_certificate_validation": "aws.acm.certificate_validation",
    "aws_cloudfront_distribution": "aws.cloudfront.distribution",
    "kubernetes_service_account": "k8s.core.v1.service_account",
    "aws_lb": "aws.elbv2.load_balancer",
    "aws_lb_target_group": "aws.elbv2.target_group",
    "aws_lb_listener": "aws.elbv2.listener",
    "aws_appautoscaling_target": "aws.application_autoscaling.scalable_target",
    "aws_placement_group": "aws.ec2.placement_group",
    "aws_appautoscaling_policy": "aws.application_autoscaling.scaling_policy",
    "aws_wafv2_web_acl": "aws.wafv2.web_acl",
    "aws_autoscaling_policy": "aws.autoscaling.scaling_policy",
    "aws_ses_identity_notification_topic": "aws.ses.identity_notification_topic",
    "aws_wafv2_regex_pattern_set": "aws.wafv2.regex_pattern_set",
    "aws_cloudformation_stack": "aws.cloudformation.stack",
    "aws_route": "aws.ec2.route",
    "random_id": "random.id",
    "random_integer": "random.integer",
    "random_password": "random.password",
    "helm_release": "helm.release",
    "null_resource": "cmd.run",
    "spotinst_ocean_aws": "spotinst.ocean.aws",
    "spotinst_ocean_aws_launch_spec": "spotinst.ocean.aws.launch_spec",
    "kubernetes_cluster_role_binding": "k8s.rbac.v1.cluster_role_binding",
    "aws_launch_template": "aws.ec2.launch_template",
}

tf_resource_type_uuid = {
    "aws_iam_role_policy": "role::name",
    "aws_iam_role_policy_attachment": "role::policy_arn",
    "aws_iam_user_policy": "user::name",
    "aws_eks_addon": "addon_name::cluster_name",
    "aws_eks_node_group": "clusterName::nodeGroupName",
    "aws_route53_zone_association": "zone_id::vpc_id::vpc_region",
    "aws_eip": "public_ip",
    "aws_acm_certificate_validation": "certificate_arn",
    "aws_appautoscaling_target": "scaling_resource_id",
    "aws_appautoscaling_policy": "policy_name",
}


tf_resource_type_default_uuid = [
    "aws_vpc",
    "aws_subnet",
    "aws_security_group",
    "aws_cloudwatch_log_group",
    "aws_db_subnet_group",
    "aws_eip",
    "aws_elasticache_subnet_group",
    "aws_flow_log",
    "aws_iam_role",
    "aws_internet_gateway",
    "aws_nat_gateway",
    "aws_route_table",
    "aws_route_table_association",
    "aws_vpc_dhcp_options_association",
    "aws_security_group_rule",
    "aws_vpc_dhcp_options",
    "aws_eks_cluster",
    "aws_iam_policy",
    "aws_iam_user",
    "aws_acm_certificate",
    "aws_iam_role_policy",
    "aws_launch_configuration",
    "aws_cloudtrail",
    "aws_cloudwatch_metric_alarm",
    "aws_config_config_rule",
    "aws_dynamodb_table",
    "aws_ami",
    "aws_ecr_repository",
    "aws_elasticache_parameter_group",
    "aws_iam_access_key",
    "aws_iam_instance_profile",
    "aws_iam_openid_connect_provider",
    "aws_iam_user_policy_attachment",
    "aws_iam_user_ssh_key",
    "aws_lambda_function",
    "aws_route53_zone",
    "aws_s3_bucket",
    "aws_s3_bucket_notification",
    "aws_s3_bucket_policy",
    "aws_sns_topic",
    "aws_sns_topic_policy",
    "aws_sns_topic_subscription",
    "aws_ec2_vpc_dhcp_options",
    "aws_iam_role",
    "aws_iam_role_policy",
    "aws_kms_key",
    "aws_rds_cluster",
    "aws_rds_cluster_instance",
    "aws_cloudwatch_event_rule",
    "aws_route53_record",
    "aws_vpc_endpoint",
    "aws_db_parameter_group",
    "aws_instance",
    "aws_kms_alias",
    "aws_rds_cluster_parameter_group",
    "aws_s3_bucket_public_access_block",
    "aws_efs_mount_target",
    "aws_eks_fargate_profile",
    "aws_efs_file_system",
    "aws_autoscaling_group",
    "aws_ec2_transit_gateway_vpc_attachment",
    "aws_api_gateway_rest_api",
    "aws_api_gateway_integration",
    "aws_lambda_permission",
    "aws_api_gateway_resource",
    "aws_cloudwatch_log_resource_policy",
    "aws_guardduty_detector",
    "aws_elasticache_replication_group",
    "aws_vpc_peering_connection",
    "aws_vpc_peering_connection_options",
    "aws_vpc_peering_connection_accepter",
    "aws_key_pair",
    "aws_api_gateway_method",
    "aws_cloudfront_distribution",
    "kubernetes_service_account",
    "aws_lb",
    "aws_lb_target_group",
    "aws_lb_listener",
    "aws_placement_group",
    "aws_wafv2_web_acl",
    "aws_autoscaling_policy",
    "aws_ses_identity_notification_topic",
    "aws_cloudformation_stack",
    "aws_wafv2_regex_pattern_set",
    "aws_route",
    "random_id",
    "random_integer",
    "random_password",
    "aws_ses_identity_notification_topic",
    "aws_cloudformation_stack",
    "aws_wafv2_regex_pattern_set",
    "aws_route",
]

FILES_TO_IGNORE = [
    "common-variables.sls",
    "variables.sls",
    "init.sls",
    "resource_ids.sls",
    "tags.sls",
]

REPLACE_COMMENT = 'ToDo: The attribute "{resource}" has terraform replace format. Please resolve the attribute value manually'

tf_equivalent_idem_attributes = {
    "aws_vpc": {"cidr_block_association_set": "cidr_block"},
    "aws_iam_role_policy": {"policy_document": "policy"},
    "aws_iam_role": {"assume_role_policy_document": "assume_role_policy"},
    "aws_s3_bucket": {"name": "bucket"},
    "aws_route53_zone": {"hosted_zone_name": "name"},
    "aws_route_table": {"routes": "route"},
    "aws_db_subnet_group": {"subnets": "subnet_ids"},
}

tf_equivalent_idem_attribute_key = {
    "aws_vpc": {
        "cidr_block_association_set": "cidr_block_association_set...[0]...CidrBlock"
    },
    "aws_iam_role_policy": {"policy_document": "policy_document"},
    "aws_iam_role": {"assume_role_policy_document": "assume_role_policy_document"},
}


def parse_tf_data(hub, path, git_dict):
    if git_dict:
        git_file = git_dict["project"].files.get(
            file_path=path, ref=hub.OPT.idem_codegen.project_branch
        )  # Open the content of *.tf file from git
        file_content = base64.b64decode(git_file.content).decode("utf-8")
        tf_data_str = file_content.replace("\\n", "\n")
        try:
            tf_data = hcl2.loads(tf_data_str)  # Parse using python-hcl2 parser
        except:
            tf_data = {}
            hub.log.warning(
                "Could not convert tf hcl to json as no resources, data or variables present in file %s",
                path,
            )
    else:
        _file = open(path)  # Open the *.tf file
        tf_data = hcl2.load(_file)  # Parse using python-hcl2 parser
        _file.close()
    return tf_data


def generate_tf_unique_value(hub, tf_uuid, attributes, tf_resource_type):
    tf_filters = [tf_uuid]
    if "::" in tf_uuid:
        tf_filters = tf_uuid.split("::")

    tf_unique_value = ""
    idem_unique_value = ""
    for tf_filter in tf_filters:
        # NOTE : If tf uuid is not properly declared in tf_resource_type_uuid, then all instances of this
        # resource type will be ignored in filtered sls data. Henceforth, in TF to SLS file conversion, such
        # resource types will not appear in SLS
        if (
            tf_filter not in attributes
            and tf_resource_type not in tf_resource_type_uuid
        ):
            return False, None, None
        tf_unique_value = (
            tf_unique_value
            + (":" if tf_unique_value else "")
            + attributes.get(tf_filter, "")
        )
        idem_resource_separator = (
            tf_resource_type_uuid_separator[tf_resource_type]
            if tf_resource_type in tf_resource_type_uuid_separator
            else "-"
        )
        idem_unique_value = (
            idem_unique_value
            + (idem_resource_separator if idem_unique_value else "")
            + attributes.get(tf_filter, "")
        )
    return True, tf_unique_value, idem_unique_value


def get_tf_equivalent_idem_attribute(
    hub, tf_resource, tf_resource_type, idem_resource_attribute
):
    if tf_resource_type in tf_equivalent_idem_attributes:
        tf_equivalent_idem_resource_attributes = tf_equivalent_idem_attributes[
            tf_resource_type
        ]
        if idem_resource_attribute in tf_equivalent_idem_resource_attributes:
            return (
                list(list(tf_resource.values())[0].values())[0].get(
                    tf_equivalent_idem_resource_attributes[idem_resource_attribute]
                ),
                tf_equivalent_idem_resource_attributes[idem_resource_attribute],
                True,
            )
    return (
        list(list(tf_resource.values())[0].values())[0].get(idem_resource_attribute),
        idem_resource_attribute,
        False,
    )


def set_tf_equivalent_idem_attribute(
    hub,
    attribute_key,
    attribute_value,
    tf_resource_type,
    idem_resource_attribute,
    resource_data,
):
    if tf_resource_type in tf_equivalent_idem_attribute_key:
        tf_equivalent_idem_resource_attributes = tf_equivalent_idem_attribute_key[
            tf_resource_type
        ]
        if idem_resource_attribute in tf_equivalent_idem_resource_attributes:
            path_arr = tf_equivalent_idem_resource_attributes[attribute_key].split(
                "..."
            )
            recent_element = resource_data
            for index_e, path_element in enumerate(path_arr):
                if index_e == len(path_arr) - 1:
                    if path_element.startswith("[") and path_element.endswith("]"):
                        path_element = int(
                            path_element.replace("[", "").replace("]", "")
                        )
                    recent_element[path_element] = attribute_value
                    continue
                if path_element.startswith("[") and path_element.endswith("]"):
                    index_of_element = int(
                        path_element.replace("[", "").replace("]", "")
                    )
                    recent_element = recent_element[index_of_element]
                else:
                    recent_element = recent_element[path_element]
    elif tf_resource_type in tf_equivalent_idem_attributes:
        tf_equivalent_idem_resource_attributes = tf_equivalent_idem_attributes[
            tf_resource_type
        ]
        if idem_resource_attribute in tf_equivalent_idem_resource_attributes:
            resource_data[idem_resource_attribute] = attribute_value


def change_bool_values_to_string(hub, complete_list_of_variables):
    for var, value in complete_list_of_variables.items():
        if isinstance(value, bool):
            complete_list_of_variables[var] = str(value)
        if "local" in var:
            if isinstance(value, dict):
                updated_dict = {}
                for local_key, local_value in value.items():
                    local_value_updated = hub.tf_idem.tool.generator.parameterizer.utils.convert_var_to_value(
                        local_value, complete_list_of_variables
                    )
                    if local_value_updated:
                        local_value = local_value_updated
                    updated_dict[local_key] = local_value
                complete_list_of_variables[var] = updated_dict
    return complete_list_of_variables


def fetch_gitlab_tf_files(hub, source, private_token, gitlab_link, project_branch):
    file_path, project = hub.tf_idem.tool.utils.fetch_project_details(
        private_token, source, gitlab_link
    )
    items = project.repository_tree(path=file_path, ref=project_branch)
    return items, file_path, project


def fetch_project_details(hub, private_token, source, gitlab_link):
    project_path = source[: source.find("//")]
    project_name = (project_path[project_path.rfind("/") + 1 :]).replace(".git", "")
    file_path_temp = source[source.rfind("//") + 1 :]
    file_path = file_path_temp[1 : file_path_temp.rfind("?")]
    gl = gitlab.Gitlab(gitlab_link, private_token=private_token)
    project_id = gl.projects.list(search=project_name, get_all=True)[0].id
    # Given the project_id
    project = gl.projects.get(project_id)
    return file_path, project
