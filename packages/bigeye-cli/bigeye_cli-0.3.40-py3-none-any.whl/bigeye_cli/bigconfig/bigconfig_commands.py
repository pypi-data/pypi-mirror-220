from pathlib import Path
from typing import Optional, List

import typer

from bigeye_cli.functions import cli_client_factory
from bigeye_cli import global_options
from bigeye_cli.bigconfig import bigconfig_options
from bigeye_sdk.controller.metric_suite_controller import MetricSuiteController
from bigeye_sdk.log import get_logger

log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help='Bigconfig Commands for Bigeye CLI')

"""
File should contain commands relating to deploying Bigconfig files.
"""

@app.command()
def plan(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        input_path: Optional[List[str]] = bigconfig_options.input_path,
        output_path: str = bigconfig_options.output_path,
        purge_source_names: Optional[List[str]] = bigconfig_options.purge_source_names,
        purge_all_sources: bool = bigconfig_options.purge_all_sources,
        no_queue: bool = bigconfig_options.no_queue,
        recursive: bool = bigconfig_options.recursive,
        strict_mode: bool = bigconfig_options.strict_mode
):
    """Executes a plan for purging sources or processing bigconfig files in the input path/current
    working directory."""

    client = cli_client_factory(bigeye_conf,config_file,workspace)
    mc = MetricSuiteController(client=client)

    # Resolve args to first true or first none None values
    if not input_path:
        input_path = client.config.bigconfig_input_path or [Path.cwd()]
    if not output_path:
        output_path = client.config.bigconfig_output_path or Path.cwd()
    strict_mode = strict_mode or client.config.bigconfig_strict_mode

    if purge_source_names or purge_all_sources:
        mc.execute_purge(purge_source_names=purge_source_names, purge_all_sources=purge_all_sources,
                         output_path=output_path, apply=False)
    else:
        mc.execute_bigconfig(input_path=input_path,
                             output_path=output_path, apply=False, recursive=recursive, 
                             no_queue=no_queue, strict_mode=strict_mode)


@app.command()
def apply(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        input_path: Optional[List[str]] = bigconfig_options.input_path,
        output_path: str = bigconfig_options.output_path,
        purge_source_names: Optional[List[str]] = bigconfig_options.purge_source_names,
        purge_all_sources: bool = bigconfig_options.purge_all_sources,
        no_queue: bool = bigconfig_options.no_queue,
        recursive: bool = bigconfig_options.recursive,
        strict_mode: bool = bigconfig_options.strict_mode,
        auto_approve: bool = bigconfig_options.auto_approve
):
    """Applies a purge of deployed metrics or applies Bigconfig files from the input path/current working directory to
    the Bigeye workspace."""

    client = cli_client_factory(bigeye_conf,config_file,workspace)
    mc = MetricSuiteController(client=client)

    # Resolve args to first true or first none None values
    if not input_path:
        input_path = client.config.bigconfig_input_path or [Path.cwd()]
    if not output_path:
        output_path = client.config.bigconfig_output_path or Path.cwd()
    strict_mode = strict_mode or client.config.bigconfig_strict_mode
    auto_approve = auto_approve or client.config.bigconfig_auto_approve

    if purge_source_names or purge_all_sources:
        mc.execute_purge(purge_source_names=purge_source_names, purge_all_sources=purge_all_sources,
                         output_path=output_path, apply=True)
    else:
        mc.execute_bigconfig(input_path=input_path, output_path=output_path, apply=True,
                             no_queue=no_queue, recursive=recursive, strict_mode=strict_mode,
                             auto_approve=auto_approve)
