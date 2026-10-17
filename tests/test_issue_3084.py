import click
from click.testing import CliRunner

import pytest


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ([], "primary"),
        (["--warehouse"], "automatic"),
        (["--warehouse", "secondary"], "secondary"),
        (["--warehouse=secondary"], "secondary"),
    ],
)
def test_optional_value_with_default(runner, args, expected):
    @click.command()
    @click.option(
        "--warehouse", is_flag=False, flag_value="automatic", default="primary"
    )
    def cli(warehouse):
        click.echo(warehouse)

    result = runner.invoke(cli, args)
    assert result.exit_code == 0, result.output
    assert result.output.strip() == expected


def test_optional_value_with_default_and_other_option(runner):
    @click.command()
    @click.option(
        "--warehouse", is_flag=False, flag_value="automatic", default="primary"
    )
    @click.option("--count", type=int, default=0)
    def cli(warehouse, count):
        click.echo(f"{warehouse} {count}")

    result = runner.invoke(cli, ["--warehouse", "--count", "3"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "automatic 3"


def test_optional_value_integer_conversion(runner):
    @click.command()
    @click.option("--port", is_flag=False, flag_value=8080, default=80)
    def cli(port):
        click.echo(f"{port} {type(port).__name__}")

    assert runner.invoke(cli, []).output.strip() == "80 int"
    assert runner.invoke(cli, ["--port"]).output.strip() == "8080 int"
    assert runner.invoke(cli, ["--port", "9090"]).output.strip() == "9090 int"


def test_optional_value_without_default(runner):
    @click.command()
    @click.option("--opt", is_flag=False, flag_value="flag")
    def cli(opt):
        click.echo(f"{opt}")

    result = runner.invoke(cli, ["--opt"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == "flag"


def test_option_without_flag_value_still_requires_value(runner):
    @click.command()
    @click.option("--name")
    def cli(name):
        click.echo(name)

    result = runner.invoke(cli, ["--name"])
    assert result.exit_code == 2
    assert "requires an argument" in result.output

    result = runner.invoke(cli, ["--name", "value"])
    assert result.exit_code == 0
    assert result.output.strip() == "value"
