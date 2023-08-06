from pathlib import Path
import tomllib as tl
import subprocess as sub

from typing import Self, List, Dict
from rich.console import Console
from rich.tree import Tree
from copy import copy

cout = Console()
cerr = Console(stderr=True)

__all__ = ['Config', 'error', 'log', 'ConfigFile', 'powershell']

Pkg = Path(__file__).parent
Root = Pkg.parent
Assets = Pkg / 'assets'
ConfigFile = Pkg / 'config.toml'



class Config:
    def __new__(cls) -> Self:
        cls.data = None
        cls.load()
        return cls
    @classmethod
    def load(cls):
        cls.data = tl.loads(ConfigFile.read_text())
    
    @classmethod        
    def render(cls):
        config = cls.data
        root = Tree("[bold red]🛠️ Configuration File[/bold red]")
        projects = root.add("[bold yellow]📦 Projects:[/bold yellow]")
        
        alias_list = config['aliases']
        
        for proot in config['projects']:
            node = projects.add(f"[magenta]🚀 {proot}[/magenta]")
            for project, aliases in alias_list.items():
                if project == proot:
                    for al in aliases:
                        node_alias = node.add(al)
                        node_alias.add(f"[underline yellow]Alias for `{proot}`.[/underline yellow]\n [dim]Use `[cyan]fr-pol-lots serve --project [red]{al}[/red][/cyan]` to launch")
        return root
    
    @classmethod
    def aliases(cls, include_name: bool = True):
        for name in cls.data['projects']:
            if include_name:
                yield name,name
            if name in cls.data['aliases']:
                for alias in cls.data['aliases'][name]:
                    yield name, alias
    
    @classmethod
    def find_project(cls, name: str) -> str:
        for project, alias in cls.aliases():
            if alias == name.lower():
                return project


def powershell(cmd: str):
    completed = sub.run(["powershell", "-Command", cmd], shell=True)

log = cout.log
error = cerr.log