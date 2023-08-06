import datetime
from typing import Optional

import typer
from rich import print
from rich.progress import track

from dinochrome_console_package.utils.klavarog import get_klavarog
from dinochrome_console_package.utils.video_duration import get_length, get_file_list

app = typer.Typer()


@app.callback()
def callback():
    """Здесь наверное должно быть какое-то краткое описание программы"""


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Подкоманда вызывается если не передано других подкоманд"""
    if ctx.invoked_subcommand is None:
        print("[bold red]Передай какие-нибудь подкоманды в командной строке![/bold red] :boom:")


# # Подкоманда вызывается с любой другой подкомандой
# @app.callback(invoke_without_command=True)
# def main():
#     print("[bold red]bla-bla-bla...[/bold red] :boom:")


@app.command()
def print_something():
    """Напечатает заранее захардкоженый текст"""
    print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")


@app.command()
def vd():
    """Показывает суммарную длительность видео в текущей папке и её подпапках"""
    file_length_list = [get_length(i) for i in track(get_file_list())]
    total_video_duration = sum(file_length_list)
    print(str(datetime.timedelta(seconds=int(total_video_duration))))


@app.command()
def kr(seed: int = typer.Argument(None)):
    """Генерирует текст на тему python для тренировки в клавиатурном тренажере"""
    get_klavarog(seed)
    print("[bold green]OK![/bold green] [green]Текст скопирован в буфер обмена[/green] 🆗")


@app.command()
def t(x: str = typer.Argument('DEFAULT')):
    print(f"Creating user: {x}")


if __name__ == "__main__":
    app()
