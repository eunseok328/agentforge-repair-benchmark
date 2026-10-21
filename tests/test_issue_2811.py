import click
from click.testing import CliRunner


def _make_command(help_name="--help"):
    def callback(ctx, param, value):
        if value:
            click.echo(f"CALLBACK={param.name}")
            ctx.exit()

    return click.Command(
        "audit",
        params=[
            click.Option(
                ["-a"], is_flag=True, expose_value=False, callback=callback
            ),
            click.Option(
                ["-b"],
                is_flag=True,
                expose_value=False,
                callback=callback,
                is_eager=True,
            ),
        ],
        context_settings={"help_option_names": [help_name]},
        callback=lambda: click.echo("NORMAL"),
    )


def _invoke(args, help_name="--help"):
    result = CliRunner().invoke(_make_command(help_name), args)
    assert result.exit_code == 0, result.output
    return result.output


def test_help_before_eager_option_wins():
    output = _invoke(["--help", "-b"])
    assert "CALLBACK=" not in output
    assert "Usage:" in output


def test_eager_option_before_help_wins():
    output = _invoke(["-b", "--help"])
    assert output == "CALLBACK=b\n"


def test_help_beats_non_eager_option_in_either_order():
    assert "CALLBACK=" not in _invoke(["--help", "-a"])
    assert "CALLBACK=" not in _invoke(["-a", "--help"])


def test_custom_help_name_ordering():
    output = _invoke(["--my-help", "-b"], help_name="--my-help")
    assert "CALLBACK=" not in output
    assert "Usage:" in output

    output = _invoke(["-b", "--my-help"], help_name="--my-help")
    assert output == "CALLBACK=b\n"


def test_normal_callback_runs_without_help():
    assert _invoke(["-a"]) == "CALLBACK=a\n"
    assert _invoke([]) == "NORMAL\n"
