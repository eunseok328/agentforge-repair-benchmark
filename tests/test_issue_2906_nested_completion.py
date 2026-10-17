"""Regression tests for nested group completion, issue #2906."""
import click
from click.shell_completion import ShellComplete


def _complete_arg(ctx, param, incomplete):
    values = ["foo", "bar", "foobar", "baz"]
    return [v for v in values if v.startswith(incomplete)]


def _build_cli():
    @click.group()
    def main():
        raise AssertionError("callback must not run during completion")

    @main.group()
    def subgroup():
        raise AssertionError("callback must not run during completion")

    @subgroup.command()
    @click.option("--name", help="Name of something.")
    @click.argument("arg", shell_complete=_complete_arg)
    def compile(name, arg):
        raise AssertionError("callback must not run during completion")

    return main


def _values(args, incomplete):
    completion = ShellComplete(_build_cli(), {}, "nested", "_NESTED_COMPLETE")
    return [c.value for c in completion.get_completions(args, incomplete)]


def test_nested_group_command_completion():
    assert _values([], "") == ["subgroup"]
    assert _values(["subgroup"], "") == ["compile"]


def test_nested_command_argument_completion():
    assert _values(["subgroup", "compile"], "") == ["foo", "bar", "foobar", "baz"]
    assert _values(["subgroup", "compile"], "f") == ["foo", "foobar"]


def test_nested_command_option_completion():
    assert _values(["subgroup", "compile"], "--") == ["--name", "--help"]
    assert _values(["subgroup", "compile"], "--n") == ["--name"]


def test_nested_command_argument_after_completed_option():
    assert _values(["subgroup", "compile", "--name=n"], "") == [
        "foo",
        "bar",
        "foobar",
        "baz",
    ]


def test_nested_command_option_value_completion():
    assert _values(["subgroup", "compile", "--name"], "") == []


def test_nested_chained_group_completion():
    @click.group(chain=True)
    def main():
        raise AssertionError("callback must not run during completion")

    @main.command()
    @click.option("--name")
    def first(name):
        raise AssertionError("callback must not run during completion")

    @main.command()
    @click.argument("arg", shell_complete=_complete_arg)
    def second(arg):
        raise AssertionError("callback must not run during completion")

    completion = ShellComplete(main, {}, "nested", "_NESTED_COMPLETE")
    assert [c.value for c in completion.get_completions(["first"], "")] == ["second"]
    assert [c.value for c in completion.get_completions(["first"], "--")] == [
        "--name",
        "--help",
    ]
    assert [c.value for c in completion.get_completions(["first", "second"], "f")] == [
        "foo",
        "foobar",
    ]
