from invoke import task
import os

def _islinux():
    """Check if operating system is Linux. 
        This is done in order to make the app Windows compatible.
    """

    return os.sys.platform.startswith('linux')

@task()
def start(ctx):
    ctx.run("python3 src/index.py", pty=_islinux())

@task()
def init(ctx):
    ctx.run("python3 src/init_database.py", pty=_islinux())

@task
def test(ctx):
    ctx.run("pytest src", pty=_islinux())

@task
def lint(ctx):
    ctx.run("pylint src", pty=_islinux())

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=_islinux())

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=_islinux())

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=_islinux())