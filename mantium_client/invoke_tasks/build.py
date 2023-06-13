"""Invoke commands for all things build!"""
from invoke import Runner, task

# Name of the repository
REPO_NAME = 'core-mantium-py'


@task
def publish_dev_build(cmd: Runner, token_name: str, token: str) -> None:
    """Publish a development build."""
    # The first step is to build the sdist and wheel
    cmd.run('poetry build')

    # TODO: (alexn) get correct package location
    # Make sure the package registry is available
    # cmd.run(f'poetry config repositories.{REPO_NAME} https://git.mantiumai.com/api/v4/projects/153/packages/pypi')

    # Set the HTTP-Auth used when connecting to GitLab's PyPI interface
    cmd.run(f'poetry config http-basic.{REPO_NAME} "{token_name}" "{token}"')

    # Now it's time to publish to the repository package registry
    cmd.run(f'poetry publish -r {REPO_NAME}')


@task
def publish_build(cmd: Runner) -> None:
    """Publish a build. Intended to be run via the GitLab CI system."""
    # The first step is to build the sdist and wheel
    cmd.run('poetry build')

    # TODO: (alexn) configure CI variables to work with this
    # Set the repo
    cmd.run(f'poetry config repositories.{REPO_NAME} ${{CI_API_V4_URL}}/projects/${{CI_PROJECT_ID}}/packages/pypi')

    # Set the repo credentials
    cmd.run(f'poetry config http-basic.{REPO_NAME} gitlab-ci-token "${{CI_JOB_TOKEN}}" ')

    # Now it's time to publish to the repository package registry
    cmd.run(f'poetry publish -r {REPO_NAME}')
