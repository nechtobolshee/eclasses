from invoke import task
import time
import threading
import socket
import os


def wait_port_is_open():
    host = os.getenv("POSTGRES_HOST")
    port = int(os.getenv("POSTGRES_PORT"))
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print("Connected to DB successfully!")
            return False
        time.sleep(1)
        print("Retrying connect to BD!")


def setup_database(ctx):
    ctx.run("./manage.py dbshell < drop_db.sql")
    ctx.run("./manage.py dbshell < db_dump.sql")
    ctx.run("./manage.py makemigrations")
    ctx.run("./manage.py migrate")


@task
def cron(ctx):
    ctx.run("python manage.py crontab add")
    ctx.run("service cron start")


@task
def run_local(ctx):
    wait_port_is_open()
    setup_database(ctx)

    thread_cron = threading.Thread(target=cron, args=(ctx,))
    thread_cron.start()

    ctx.run("./manage.py collectstatic --noinput")
    ctx.run("./manage.py runserver 0.0.0.0:8000")
