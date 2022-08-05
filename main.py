#!/usr/bin/python3

import click


@click.group()
def cli():
    pass


@cli.command(name='send_message')
def init_db():
    print("init db ")


@cli.command(name='run_app')
def app():
    from process import app_run
    app_run()


if __name__ == '__main__':
    cli()
