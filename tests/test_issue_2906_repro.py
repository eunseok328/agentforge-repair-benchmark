"""Nested command options should complete at the current command."""
import click
from click.shell_completion import ShellComplete


def test_nested_command_option_completion():
    cli = click.Group('tool', commands=[click.Group('manage', commands=[
        click.Command('build', params=[click.Option(['--name'])])])])
    completion = ShellComplete(cli, {}, 'tool', '_TOOL_COMPLETE')
    actual = [c.value for c in completion.get_completions(['manage', 'build'], '--n')]
    assert actual == ['--name']
