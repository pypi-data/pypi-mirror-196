import yaml
import os
import argparse
import click
from dlt.common.pipeline import get_default_pipelines_dir
from dlt.common.runners.stdout import iter_stdout
from dlt.common.runners.venv import Venv
from dlt.common.storages.file_storage import FileStorage

from dlt.version import __version__
from dlt.common import json
from dlt.common.schema import Schema
from dlt.common.typing import DictStrAny

from dlt.pipeline import attach

import dlt.cli.echo as fmt
from dlt.cli import utils
from dlt.cli.init_command import init_command, list_pipelines_command, DLT_INIT_DOCS_URL, DEFAULT_PIPELINES_REPO
from dlt.cli.deploy_command import PipelineWasNotRun, deploy_command, DLT_DEPLOY_DOCS_URL
from dlt.pipeline.exceptions import CannotRestorePipelineException


def init_command_wrapper(pipeline_name: str, destination_name: str, use_generic_template: bool, repo_location: str, branch: str) -> int:
    try:
        init_command(pipeline_name, destination_name, use_generic_template, repo_location, branch)
    except Exception as ex:
        click.secho(str(ex), err=True, fg="red")
        fmt.note("Please refer to %s for further assistance" % fmt.bold(DLT_INIT_DOCS_URL))
        raise
    return 0


def list_pipelines_command_wrapper(repo_location: str, branch: str) -> int:
    try:
        list_pipelines_command(repo_location, branch)
    except Exception as ex:
        click.secho(str(ex), err=True, fg="red")
        fmt.note("Please refer to %s for further assistance" % fmt.bold(DLT_INIT_DOCS_URL))
        return -1
    return 0


def deploy_command_wrapper(pipeline_script_path: str, deployment_method: str, schedule: str, run_on_push: bool, run_on_dispatch: bool, branch: str) -> int:
    try:
        utils.ensure_git_command("deploy")
    except Exception as ex:
        click.secho(str(ex), err=True, fg="red")
        return -1

    from git import InvalidGitRepositoryError, NoSuchPathError
    try:
        deploy_command(pipeline_script_path, deployment_method, schedule, run_on_push, run_on_dispatch, branch)
    except (CannotRestorePipelineException, PipelineWasNotRun) as ex:
        click.secho(str(ex), err=True, fg="red")
        fmt.note("You must run the pipeline locally successfully at least once in order to deploy it.")
        fmt.note("Please refer to %s for further assistance" % fmt.bold(DLT_DEPLOY_DOCS_URL))
        return -1
    except InvalidGitRepositoryError:
        click.secho(
            "No git repository found for pipeline script %s.\nAdd your local code to Github as described here: %s" % (fmt.bold(pipeline_script_path), fmt.bold("https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github")),
            err=True,
            fg="red"
        )
        fmt.note("Please refer to %s for further assistance" % fmt.bold(DLT_DEPLOY_DOCS_URL))
        return -1
    except NoSuchPathError as path_ex:
        click.secho(
            "The pipeline script does not exist\n%s" % str(path_ex),
            err=True,
            fg="red"
        )
        return -1
    except Exception as ex:
        click.secho(str(ex), err=True, fg="red")
        fmt.note("Please refer to %s for further assistance" % fmt.bold(DLT_DEPLOY_DOCS_URL))
        # TODO: display stack trace if with debug flag
        raise
    return 0


def pipeline_command_wrapper(operation: str, name: str, pipelines_dir: str) -> int:

    try:
        if operation == "list":
            pipelines_dir = pipelines_dir or get_default_pipelines_dir()
            storage = FileStorage(pipelines_dir)
            dirs = storage.list_folder_dirs(".", to_root=False)
            if len(dirs) > 0:
                click.echo("%s pipelines found in %s" % (len(dirs), fmt.bold(pipelines_dir)))
            else:
                click.echo("No pipelines found in %s" % fmt.bold(pipelines_dir))
            for _dir in dirs:
                click.secho(_dir, fg="green")
            return 0

        p = attach(pipeline_name=name, pipelines_dir=pipelines_dir)
        click.echo("Found pipeline %s in %s" % (fmt.bold(p.pipeline_name), fmt.bold(p.pipelines_dir)))

        if operation == "show":
            from dlt.helpers import streamlit
            venv = Venv.restore_current()
            for line in iter_stdout(venv, "streamlit", "run", streamlit.__file__, name):
                click.echo(line)

        if operation == "info":
            state = p.state
            for k, v in state.items():
                if not isinstance(v, dict):
                    click.echo("%s: %s" % (click.style(k, fg="green"), v))
            for k, v in state["_local"].items():
                if not isinstance(v, dict):
                    click.echo("%s: %s" % (click.style(k, fg="green"), v))

        if operation == "failed_loads":
            completed_loads = p.list_completed_load_packages()
            for load_id in completed_loads:
                click.echo("Checking failed jobs in load id '%s'" % fmt.bold(load_id))
                for job, failed_message in p.list_failed_jobs_in_package(load_id):
                    click.echo("JOB: %s" % fmt.bold(os.path.abspath(job)))
                    click.secho(failed_message, fg="red")

        if operation == "sync":
            if click.confirm("About to drop the local state of the pipeline and reset all the schemas. The destination state, data and schemas are left intact. Proceed?", default=False):
                p = p.drop()
                p.sync_destination()
        return 0
    except (CannotRestorePipelineException, Exception) as ex:
        click.secho(str(ex), err=True, fg="red")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Runs various DLT modules", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    subparsers = parser.add_subparsers(dest="command")

    init_cmd = subparsers.add_parser("init", help="Adds or creates a pipeline in the current folder.")
    init_cmd.add_argument("--list-pipelines", "-l",  default=False, action="store_true", help="List available pipelines")
    init_cmd.add_argument("pipeline", nargs='?', help="Pipeline name. Adds existing pipeline or creates a new pipeline template if pipeline for your data source is not yet implemented.")
    init_cmd.add_argument("destination", nargs='?', help="Name of a destination ie. bigquery or redshift")
    init_cmd.add_argument("--location", default=DEFAULT_PIPELINES_REPO, help="Advanced. Uses a specific url or local path to pipelines repository.")
    init_cmd.add_argument("--branch", default=None, help="Advanced. Uses specific branch of the init repository to fetch the template.")
    init_cmd.add_argument("--generic", default=False, action="store_true", help="When present uses a generic template with all the dlt loading code present will be used. Otherwise a debug template is used that can be immediately run to get familiar with the dlt sources.")

    deploy_cmd = subparsers.add_parser("deploy", help="Creates a deployment package for a selected pipeline script")
    deploy_cmd.add_argument("pipeline_script_path", help="Path to a pipeline script")
    deploy_cmd.add_argument("deployment_method", choices=["github-action"], default="github-action", help="Deployment method")
    deploy_cmd.add_argument("--schedule", required=True, help="A schedule with which to run the pipeline, in cron format. Example: '*/30 * * * *' will run the pipeline every 30 minutes.")
    deploy_cmd.add_argument("--run-manually", default=True, action="store_true", help="Allows the pipeline to be run manually form Github Actions UI.")
    deploy_cmd.add_argument("--run-on-push", default=False, action="store_true", help="Runs the pipeline with every push to the repository.")
    deploy_cmd.add_argument("--branch", default=None, help="Advanced. Uses specific branch of the deploy repository to fetch the template.")

    schema = subparsers.add_parser("schema", help="Shows, converts and upgrades schemas")
    schema.add_argument("file", help="Schema file name, in yaml or json format, will autodetect based on extension")
    schema.add_argument("--format", choices=["json", "yaml"], default="yaml", help="Display schema in this format")
    schema.add_argument("--remove-defaults", action="store_true", help="Does not show default hint values")

    pipe_cmd = subparsers.add_parser("pipeline", help="Operations on pipelines that were ran locally")
    pipe_cmd.add_argument("name", help="Pipeline name")
    pipe_cmd.add_argument(
        "operation",
        choices=["info", "show", "list", "failed_loads", "sync"],
        default="info",
        help="""'info' - displays state of the pipeline,
'show' - launches streamlit app with the loading status and dataset explorer,
'failed_loads' - displays information on all the failed loads, failed jobs and associated error messages,
'sync' - drops the local state of the pipeline and resets all the schemas and restores it from destination. The destination state, data and schemas are left intact."""
    )
    pipe_cmd.add_argument("--pipelines_dir", help="Pipelines working directory", default=None)

    args = parser.parse_args()

    if args.command == "schema":
        with open(args.file, "br") as f:
            if os.path.splitext(args.file)[1][1:] == "json":
                schema_dict: DictStrAny = json.load(f)
            else:
                schema_dict = yaml.safe_load(f)
        s = Schema.from_dict(schema_dict)
        if args.format == "json":
            schema_str = json.dumps(s.to_dict(remove_defaults=args.remove_defaults), pretty=True)
        else:
            schema_str = s.to_pretty_yaml(remove_defaults=args.remove_defaults)
        print(schema_str)
    elif args.command == "pipeline":
        return pipeline_command_wrapper(args.operation, args.name, args.pipelines_dir)
    elif args.command == "init":
        if args.list_pipelines:
            return list_pipelines_command_wrapper(args.location, args.branch)
        else:
            if not args.pipeline or not args.destination:
                init_cmd.print_usage()
                return -1
            else:
                return init_command_wrapper(args.pipeline, args.destination, args.generic, args.location, args.branch)
    elif args.command == "deploy":
        return deploy_command_wrapper(args.pipeline_script_path, args.deployment_method, args.schedule, args.run_on_push, args.run_manually, args.branch)
    else:
        parser.print_help()
        return -1
    return 0


def _main() -> None:
    exit(main())


if __name__ == "__main__":
    exit(main())
