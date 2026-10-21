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

import pytest

@pytest.mark.parametrize('args,name,winner',[(('--my-help','-b'),'--my-help','help'),(('-b','--my-help'),'--my-help','b'),(('-a','--my-help'),'--my-help','help'),(('--my-help','-a'),'--my-help','help'),(('-a',),'--my-help','a'),(('-a','-b'),'--my-help','b'),(('--assist','-b'),'--assist','help'),((),'--my-help','normal')])
def test_approved_contract(args,name,winner):
    output=exercise(args,name)
    if winner=='help': assert name in output and 'CALLBACK=' not in output
    elif winner=='normal': assert 'NORMAL' in output
    else: assert 'CALLBACK='+winner in output
