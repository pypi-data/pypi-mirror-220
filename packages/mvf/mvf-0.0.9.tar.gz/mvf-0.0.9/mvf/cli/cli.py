import click
import os
import sys
from mvf.cli import utils
from mvf.dag.builder import DagBuilder
from mvf.template.config import ConfigBuilder
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
import logging
rpy2_logger.setLevel(logging.ERROR)


@click.group(
    help='''
    MVF

    See the documentation: 

        https://tomkimcta.gitlab.io/model-validation-framework
    '''
)
def mvf():
    '''
    CLI entry point.
    '''
    # Add working directory to PYTHONPATH to allow import of local modules
    sys.path.append(os.getcwd())


@click.command(
    help='''
        Try out an example project.
    '''
)
@click.option(
    '--list',
    '-l',
    is_flag=True,
    default=False,
    help='List the available projects.'
)
@click.option(
    '--name',
    '-n',
    default=None,
    help='Name of project to download.'
)
@click.option(
    '--output',
    '-o',
    default=None,
    help='Target directory.'
)
def examples(list, name, output):
    # Use this list to manage which examples to expose
    examples_list = [
        'feature_scaling',
        'py_preprocess_train_test',
        'r_preprocess_kfold'
    ]
    if list:
        # List the examples in the console
        click.echo('The available examples are\n')
        for example_name in examples_list:
            click.echo(f'    {example_name}')
        click.echo('\nDownload them using `mvf examples -n name_of_project')
    elif name is None:
        # Print the help text
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
    else:
        # Try download the example called name
        if name in examples_list:
            click.echo(f'Downloading {name} project...')
            # Download the example
            output_dir = output if output is not None else name
            utils.download_example(name, output_dir)
        else:
            click.echo(
                f'There is no project named {name}. Check the available projects with\n\n  mvf examples -l\n')


@click.command(
    help='''
        Utility for initialising an MVF project. Generates an MVF
        configuration file. Default use will initialise the MVF
        project in the current working directory.
    '''
)
@click.option(
    '--directory',
    '-d',
    default='.',
    help='The directory in which to initialise the MVF project.'
)
def init(directory):
    # check if default use
    if directory == '.':
        pth = os.getcwd()
        click.echo('Initialising MVF project in the current working directory')
    # path specified by user
    else:
        if os.path.isabs(directory):
            pth = directory
        # if relative path provided, construct absolute
        else:
            pth = os.path.join(
                os.getcwd(),
                directory
            )
        # check if the path provided by the user is already a file
        if os.path.isfile(pth):
            raise click.ClickException(
                'A file already exists at the location provided!')
        click.echo(f'Initialising MVF project in {pth}')
    # get confirmation from user
    click.confirm(f'Do you want to continue?', abort=True)
    cfg_builder = ConfigBuilder(pth)
    cfg_builder.write()


@click.command(
    help='''
        Utility for running MVF projects or processes. Default use
        will trigger an incremental execution of the project.
    '''
)
@click.option(
    '--force',
    '-f',
    is_flag=True,
    default=False,
    help="Force execution of whole workflow."
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Specify the output directory.'
)
@click.option(
    '--process',
    '-p',
    default=None,
    help='Force execution of a specific process by name.'
)
def run(force, output, process):
    # load project config
    config = utils.load_config(
        os.path.join(
            os.getcwd(),
            'mvf_conf.yaml'
        )
    )
    # build dag from config
    click.echo('Building MVF project workflow...')
    dag_builder = DagBuilder(config, output_dir=output)
    dag_builder.build()
    if process is None:
        # access the built dag and execute it
        click.echo('Running MVF project...')
        dag_builder.dag.build(force=force)
    else:
        # access a process and execute it
        dag_process = dag_builder.dag.get(process)
        dag_builder.dag.render(force=force)
        click.echo(f'Running {process} process...')
        dag_process.build(force=True)
    # plot the dag
    click.echo('Plotting workflow...')
    dag_builder.dag.plot('project_workflow.html')


@click.command(
    help='''
        Utility for plotting MVF workflows. If saving outputs to a
        custom directory, this directory should be passed as an
        option to get up-to-date process statuses.
    '''
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Specify the output directory.'
)
def plot(output):
    # load project config
    config = utils.load_config(
        os.path.join(
            os.getcwd(),
            'mvf_conf.yaml'
        )
    )
    # build dag from config
    dag_builder = DagBuilder(config, output_dir=output)
    dag_builder.build()
    click.echo('Plotting workflow...')
    # access the built dag and plot it
    dag_builder.dag.plot('project_workflow.html')


# add commands to group
mvf.add_command(examples)
mvf.add_command(run)
mvf.add_command(plot)
mvf.add_command(init)
