from invoke import task

@task
def read_sudokus(ctx):
    ctx.run("python3 src/read_sudokus.py", pty=True)

@task(read_sudokus)
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)

@task()
def init(ctx):
    ctx.run("python3 src/init_database.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)