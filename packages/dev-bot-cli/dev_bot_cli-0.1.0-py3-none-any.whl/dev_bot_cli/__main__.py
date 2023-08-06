import click

from dev_bot_cli.command.prune_remote import PruneRemote


@click.group()
def cli():
    pass


@cli.command()
@click.option('--repo',  default='.', type=click.Path(exists=True, resolve_path=True))
@click.option('--remote', default='origin', type=click.STRING)
@click.option('--branch', default='master', type=click.STRING)
def prune_remote(repo, remote, branch):
    click.secho(f'> Pruning of merged branches with {branch}', fg='green')
    command = PruneRemote(repository_path=repo, remote_name=remote, current_branch=branch)
    branches = command.get_remote_merged_branches()

    if not branches:
        click.secho('> No merged branches found', fg='yellow')
        return

    click.secho('> The following branches will be deleted:', fg='green')
    for b in branches:
        click.secho(f'\t> {b}', fg='green')

    if click.confirm(click.style('> Do you want to continue?', fg='green')):
        command.remove_branches(branches)
        click.secho('> Removed successfully', fg='green')
