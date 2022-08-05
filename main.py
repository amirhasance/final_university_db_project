#!/usr/bin/python3

import click


@click.group()
def cli():
    pass


@cli.command(name='run_app')
def app():
    from process import app_run
    app_run()


if __name__ == '__main__':
    cli()
