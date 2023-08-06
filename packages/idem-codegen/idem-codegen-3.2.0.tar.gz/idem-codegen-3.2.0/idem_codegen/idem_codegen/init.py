def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # The run.py is where your app should usually start
    hub.pop.sub.load_subdirs(hub.idem_codegen, recurse=True)
    hub.idem_codegen.RUNS = {}
    hub.pop.sub.add(dyne_name="tf_idem")
    hub.pop.sub.add(dyne_name="discovery")
    hub.pop.sub.add(dyne_name="states")
    hub.pop.sub.add(dyne_name="idem_data_insights")
    hub.pop.sub.load_subdirs(hub.states, recurse=True)


def cli(hub):
    hub.pop.config.load(["idem_codegen"], cli="idem_codegen")
    # Your app's options can now be found under hub.OPT.idem_codegen
    kwargs = dict(hub.OPT.idem_codegen)
    hub.test = None

    # Initialize the asyncio event loop
    hub.pop.loop.create()

    # Start the async code
    coroutine = hub.idem_codegen.init.run(**kwargs)
    hub.pop.Loop.run_until_complete(coroutine)


async def run(hub, **kwargs):
    global run_name
    try:
        if hub.test:
            run_name = hub.test.idem_codegen.run_name
        elif hub.SUBPARSER == "generate":
            # if (
            #     hub.OPT.idem_codegen.type
            #     not in hub.idem_codegen.tool.utils.ACCEPTABLE_GENERATE_TYPES
            # ):
            #     raise ValueError("Invalid value of parameter 'type'")
            if hub.OPT.idem_codegen.type == "resource_ids":
                hub.log.info("Idem Resource Id files Generation started")
                hub.tf_idem.exec.generate_resource_ids_from_tf_state.init()
                hub.log.info("Idem Resource Id files Generation completed")
            elif hub.OPT.idem_codegen.type == "terraform_drift":
                hub.log.info("Idem describe script Generation started")
                await hub.tf_idem.exec.generate_terraform_drift.init()
                hub.log.info("Idem describe script Generation completed")
            elif hub.OPT.idem_codegen.type == "idem_describe_script":
                hub.log.info("Idem describe script Generation started")
                hub.tf_idem.exec.generate_idem_describe_script_from_tf_state.init()
                hub.log.info("Idem describe script Generation completed")
            else:
                hub.log.info("Idem Resource Id files Generation started")
                hub.tf_idem.exec.generate_any_attribute_from_state_file.init()
                hub.log.info("Idem Resource Id files Generation completed")
            print("Generation completed.")
            return
        elif hub.SUBPARSER in hub.idem_codegen.tool.utils.ACCEPTABLE_RUN_NAMES:
            hub.log.info(
                f"Idem Codegen {hub.SUBPARSER} started",
            )
            run_name = hub.SUBPARSER
        else:
            raise ValueError("Invalid value of parameter 'run_name'")
    except Exception as e:
        hub.log.error(e)
        return

    """
    This is the entrypoint for the async code in your project
    """
    stages = ["validate", "compile", "group", "generate"]
    progress_bar = hub.idem_codegen.tool.progress.init.create(
        stages, desc=f"idem codegen", unit="states", colour="#FFFFFF", smoothing=0.3
    )

    progress_bar.set_description("Validate phase started")
    progress_bar.refresh()
    hub.idem_codegen.validator.init.validate(run_name)
    progress_bar.set_description("Validate phase completed successfully")
    progress_bar.refresh()

    hub.idem_codegen.tool.progress.init.update(progress_bar)
    progress_bar.set_description("Compile phase started")
    progress_bar.refresh()
    await hub.idem_codegen.compiler.init.compile(run_name)
    progress_bar.set_description("Compile phase completed successfully")
    progress_bar.refresh()
    hub.idem_codegen.tool.progress.init.update(progress_bar)
    progress_bar.set_description("Group phase started")
    progress_bar.refresh()

    # Preprocessing is completed now. Starting with file by file conversion for each module in cluster
    output_dir_path = hub.idem_codegen.group[
        hub.OPT.idem_codegen.group_style
    ].segregate(run_name)

    progress_bar.set_description("Group phase completed successfully")
    progress_bar.refresh()
    hub.idem_codegen.tool.progress.init.update(progress_bar)
    progress_bar.set_description("Generation phase started")
    progress_bar.refresh()
    # Generation Phase
    hub.idem_codegen.generator.init.run(run_name, output_dir_path)
    hub.log.info("Idem Code Generation completed")

    hub.idem_codegen.tool.progress.init.update(progress_bar)
    progress_bar.set_description("Generation phase completed successfully")
    progress_bar.refresh()
