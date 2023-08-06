import click
import shutil
from .setting import *
from .temp import create_folder_file

@click.group()
def cli():
    pass

@cli.command(name='tiny', help='Build a tiny python project.')
@click.option('--name', default='myPythonProject', help='The name for your python project.')
@click.option('--demo', default=False, help='An example of project.')
def tiny_project(name: str, demo: bool):
    if demo:
        create_demo()
    
    meta_data.update({"repo_name": name})
    create_folder_file(templates_dir=templates_dir, meta_data=meta_data, **tiny)


@cli.command(name='basic', help='Build a tiny python project.')
@click.option('--name', default='myPythonProject', help='The name for your python project.')
@click.option('--demo', default=False, help='An example of project.')
def basic_project(name: str, demo: bool):
    if demo:
        create_demo()
    
    meta_data.update({"repo_name": name})
    create_folder_file(templates_dir=templates_dir, meta_data=meta_data, **basic)


if __name__ == '__main__':
    cli()