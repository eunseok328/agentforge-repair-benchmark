import click
from click.testing import CliRunner


def test_optional_warehouse_value():
    @click.command()
    @click.option("--warehouse", is_flag=False,
                  flag_value="automatic", default="primary")
    def cli(warehouse):
        click.echo(warehouse)

    result = CliRunner().invoke(cli, ["--warehouse"])
    assert result.exit_code == 0, result.output
    assert result.output == "automatic\n"
