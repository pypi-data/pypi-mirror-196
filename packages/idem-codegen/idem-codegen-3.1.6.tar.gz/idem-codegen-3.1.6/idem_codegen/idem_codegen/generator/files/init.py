import os
from os.path import exists
from typing import Any
from typing import Dict

from idem_codegen.idem_codegen.tool.utils import MyDumperNoBlankLines

sub_dirs_to_ignore = ["params", "sls"]


def generate(hub, module_output_directory_path: str, sls_data: Dict[str, Any]):
    for root, subdirectories, files in os.walk(module_output_directory_path):
        for subdirectory in subdirectories:
            if subdirectory == "params":
                hub.idem_codegen.generator.files["0020_initial"].create(
                    subdirectory, os.path.join(root, subdirectory), sls_data
                )
                if exists(os.path.join(root, "params/variables.sls")):
                    variables_data = hub.idem_codegen.tool.utils.parse_sls_data(
                        os.path.join(root, "params/variables.sls")
                    )
                    variables_data = {
                        k: v
                        for k, v in variables_data.items()
                        if k not in hub.idem_codegen.RUNS["COMMON_VARIABLES"]
                    }
                    variables_data["include"] = ["common-variables"]
                    hub.idem_codegen.tool.utils.dump_sls_data_to_file(
                        os.path.join(root, "params/variables.sls"),
                        variables_data,
                        dumper=MyDumperNoBlankLines,
                    )
                continue
            if subdirectory in sub_dirs_to_ignore:
                continue
            sls_data_of_module = (
                hub.idem_codegen.exec.generator.generate.collect_sls_data_in_folder(
                    os.path.join(module_output_directory_path, subdirectory, "sls"),
                    sls_data,
                )
            )
            # hub.idem_codegen.tool.utils.recursively_iterate_sls_files_directory(
            #     os.path.join(module_output_directory_path, subdirectory, "sls"),
            #     hub.idem_codegen.exec.generator.generate.collect_sls_data_in_folder,
            #     sls_data_of_module=sls_data_of_module,
            #     sls_data=sls_data
            # )

            for file_generator_plugin in sorted(
                hub.idem_codegen.generator.files._loaded.keys()
            ):
                if file_generator_plugin == "init":
                    continue

                hub.idem_codegen.generator.files[file_generator_plugin].create(
                    subdirectory,
                    os.path.join(module_output_directory_path, subdirectory),
                    sls_data_of_module,
                )
    if "COMMON_VARIABLES" in hub.idem_codegen.RUNS:
        hub.idem_codegen.tool.utils.dump_sls_data_to_file(
            f"{module_output_directory_path}/common-variables.sls",
            hub.idem_codegen.RUNS["COMMON_VARIABLES"],
            dumper=MyDumperNoBlankLines,
        )
