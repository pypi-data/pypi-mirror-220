import typer
import sys
import os


from .server.government_spending import Dashboard as gvt_spend
from .utils import Config, Pkg, Root, Path, error, log, powershell

cli = typer.Typer(
    name='fr-pol-plots',
    help='Make interactive plots about french politics.',
    no_args_is_help=True
    )


@cli.command("serve", help='Create a `dash` app to serve the data pertaining to `project`')
def serve(
    project:str = typer.Option(None, '-P', '--project', help='Project name to generate dash app for.'),
    debug: bool = typer.Option(False, '-d', '--debug', help='Dash debug mode'),
    host: str = typer.Option("127.0.0.1", '-h', '--host', help='Dash server host'),
    port: str = typer.Option("8050", '-p', '--port', help='Dash server port')
    ):
    config = Config()

    name = config.find_project(project)
    
    match name:
        case 'lfi-spending':
            app = gvt_spend.make()
        case _:
            app = gvt_spend.make()
            
            
    app.run(port=port, host=host, debug=debug)
    
@cli.command("ls", help="List project names.")
def list_items():
    config = Config()
    log(config.render())

@cli.command("pack", help="Make a new procfile for Heroku hosting & create `requirements.txt`.", no_args_is_help=True)
def make_procfile(
    project:str = typer.Option(None, '-P', '--project', help='Project name to generate dash app for.'),
    ):
    config = Config()
    
    name = config.find_project(project)
    procfiles = config.data['procfiles']
    content = procfiles[name] if name in procfiles else error(f"[bold red]📢 Procfile not found:[/bold red] [yellow]project = {name} has no procfile.[/yellow]")
    
    if not content:
        typer.Exit(1)
    else:
        procfile = (Root / 'Procfile')
        procfile.write_text(content)
        log(f"[bold green]✅ Done. [/bold green] [yellow]Wrote new Procfile to {procfile}[/yellow]")
    
    if sys.platform == 'win32':
        cmd = "poetry export --without-hashes --format=requirements.txt | Out-File -FilePath requirements.txt"
        powershell(cmd)
    else:
        cmd = "poetry export --without-hashes --format=requirements.txt > requirements.txt"
        os.system(cmd)
        
    log(f"[bold green]✅ Done. [/bold green] [yellow]Wrote new `requirements.txt`[/yellow]")