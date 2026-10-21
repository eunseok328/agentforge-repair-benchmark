import click
from click.testing import CliRunner
def exercise(args=('--my-help','-b'),name='--my-help'):
    def callback(ctx,param,value):
        if value:
            click.echo('CALLBACK='+param.name)
            ctx.exit()
    command=click.Command('audit',params=[
        click.Option(['-a'],is_flag=True,expose_value=False,callback=callback),
        click.Option(['-b'],is_flag=True,expose_value=False,callback=callback,is_eager=True)],
        context_settings={'help_option_names':[name]},callback=lambda:click.echo('NORMAL'))
    result=CliRunner().invoke(command,list(args))
    assert result.exit_code==0,result.output
    return result.output

def test_public_behavior():
    assert "CALLBACK=" not in exercise(('--my-help',"-b"),'--my-help')
