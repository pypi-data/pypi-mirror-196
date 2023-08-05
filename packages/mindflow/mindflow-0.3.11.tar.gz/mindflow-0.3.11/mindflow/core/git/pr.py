import concurrent.futures
import subprocess
from typing import List

from mindflow.core.git.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import PR_BODY_PREFIX
from mindflow.utils.prompts import PR_TITLE_PREFIX


def run_pr():
    # Get the name of the current branch
    current_branch = (
        subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])
        .decode("utf-8")
        .strip()
    )

    # Determine the name of the default branch
    default_branch = (
        subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
        .decode()
        .strip()
        .split("/")[-1]
    )

    if current_branch == default_branch:
        print("Cannot create pull request from default branch")
        return

    if not has_remote_branch(current_branch):
        print("No remote branch for current branch")
        return

    if needs_push():
        print("Current branch needs to be pushed to remote repository")
        return

    settings = Settings()

    diff_output = run_diff((default_branch,))

    pr_title_prompt = build_context_prompt(PR_TITLE_PREFIX, diff_output)
    pr_body_prompt = build_context_prompt(PR_BODY_PREFIX, diff_output)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_title = executor.submit(
            settings.mindflow_models.query.model, pr_title_prompt
        )
        future_body = executor.submit(
            settings.mindflow_models.query.model, pr_body_prompt
        )

    pr_title = future_title.result()
    pr_body = future_body.result()

    create_pull_request(pr_title, pr_body)


def needs_push() -> bool:
    """
    Returns True if the current branch needs to be pushed to a remote repository, False otherwise.
    """
    # Get the output of `git status`
    git_status = subprocess.check_output(["git", "status"]).decode("utf-8")

    # Check if the output contains the message "Your branch is ahead of 'origin/<branch>' by <num> commit(s), and can be fast-forwarded."
    return "Your branch is ahead of" in git_status


def has_remote_branch(current_branch: str) -> bool:
    """
    Returns True if there is a remote branch for the current branch, False otherwise.
    """
    # Check if there is a remote branch for the current branch
    try:
        subprocess.check_output(
            ["git", "ls-remote", "--exit-code", "--heads", "origin", current_branch]
        )
        return True
    except subprocess.CalledProcessError:
        return False


def create_pull_request(title, body):
    command: List[str] = ["gh", "pr", "create", "--title", title, "--body", body]  # type: ignore
    pr_result = subprocess.check_output(command).decode("utf-8")
    if "https://" in pr_result:
        print("Pull request created successfully")
        print(pr_result)
    else:
        print(
            "Failed to create pull request. Please raise an issue at: https://github.com/nollied/mindflow-cli/issues"
        )
        exit()
