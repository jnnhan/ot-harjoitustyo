from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)

@task
def init(ctx):
    ctx.run("python3 src/init_database.py", pty=True)