import ast
import os
from pathlib import Path
import sys
import tempfile
from importlib import import_module
from types import ModuleType

from dlt.common import git
from dlt.common.reflection.utils import set_ast_parents
from dlt.common.storages import FileStorage

from dlt.reflection.script_visitor import PipelineScriptVisitor

from dlt.cli.exceptions import CliCommandException


COMMAND_REPO_LOCATION = "https://github.com/dlt-hub/python-dlt-%s-template.git"
REQUIREMENTS_TXT = "requirements.txt"
PYPROJECT_TOML = "pyproject.toml"
GITHUB_WORKFLOWS_DIR = os.path.join(".github", "workflows")
LOCAL_COMMAND_REPO_FOLDER = "repos"
MODULE_INIT = "__init__.py"


def clone_command_repo(command: str, branch: str) -> FileStorage:
    template_dir = tempfile.mkdtemp()
    # TODO: handle ImportError (no git command available) gracefully
    with git.clone_repo(COMMAND_REPO_LOCATION % command, template_dir, branch=branch):
        return FileStorage(template_dir)


def parse_init_script(command: str, script_source: str, init_script_name: str) -> PipelineScriptVisitor:
    # parse the script first
    tree = ast.parse(source=script_source)
    set_ast_parents(tree)
    visitor = PipelineScriptVisitor(script_source)
    visitor.visit_passes(tree)
    if len(visitor.mod_aliases) == 0:
        raise CliCommandException(command, f"The pipeline script {init_script_name} does not import dlt and does not seem to run any pipelines")

    return visitor


def ensure_git_command(command: str) -> None:
    try:
        import git
    except ImportError as imp_ex:
        if "Bad git executable" not in str(imp_ex):
            raise
        raise CliCommandException(
            command,
            "'git' command is not available. Install and setup git with the following the guide %s" % "https://docs.github.com/en/get-started/quickstart/set-up-git",
            imp_ex
        ) from imp_ex
