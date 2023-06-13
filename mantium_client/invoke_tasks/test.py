"""Invoke tasks for testing."""

from invoke import Runner, task


@task
def run(c: Runner) -> None:
    """Execute pytest for the API."""
    c.run('pytest tests/', pty=True)
