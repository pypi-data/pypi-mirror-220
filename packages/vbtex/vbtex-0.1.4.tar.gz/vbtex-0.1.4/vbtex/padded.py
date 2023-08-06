
import click
import os
import sys
from rich.console import Console
from .choice_option import ChoiceOption



@click.command(
    help="Renders tex expressions into pdf"
)
@click.option(
    '-p',
    '--padding',
    type = click.INT,
    default=1,
    show_default=True,
    help="Format of the output"
)
def padded(padding):
    tex = click.edit()
    click.echo(tex)
    
    os.makedirs(f'./vbtex', exist_ok=True)
    path_main = os.path.join(f'./vbtex', 'main.tex')

    
    with open(path_main, 'w') as file:
        file.write(f'\\documentclass[preview, margin={padding} mm]{{standalone}}\n')
        file.write(f'\\usepackage{{v-equation}}\n')
        file.write(f'\\begin{{document}}\n')

        file.write(f'\\vspace*{{\\fill}}\n\n')
        file.write(f'\\begin{{center}}\n')
        file.write(f'{tex}\n')
        file.write(f'\\end{{center}}\n')
        file.write(f'\\vspace*{{\\fill}}\n\n')
        file.write(f'\\end{{document}}')



    try:
        os.chdir("./vbtex")
        try:
            os.system("pdflatex -shell-escape main.tex")
        except:
            click.echo("Failed to rum pdflatex")
    except:
        click.echo("Failed to run cddir") 


    


