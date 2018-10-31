from invoke import task

@task
def hello(c):
    c.run("echo 'hello fabric'")
    print("hello world")
