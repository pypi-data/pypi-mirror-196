import glob
from pathlib import Path

import libcst as cst
import typer

from printcleaner.transformer import PrintTransformer

app = typer.Typer()


@app.command()
def main(target: Path):
    if not target.exists():
        typer.echo("Invalid path. Please supply a valid path.")
        raise typer.Exit(code=1)
    elif target.is_file():
        remove_print_statements(target)
        typer.echo(f"Successfully removed print statements from file.")
    elif target.is_dir():
        all_python_files = get_all_python_files(target)
        result = list(map(remove_print_statements, all_python_files))
        typer.echo(
            "Successfully removed print statements from {} file(s).".format(len(result))
        )


def remove_print_statements(file_path: Path):
    file = open(file_path, "r")
    code = file.read()
    modified_tree = transform_tree(code)
    with open(file_path, "w") as f:
        f.write(modified_tree)


def transform_tree(code: str) -> str:
    tree = cst.parse_module(code)
    transformer = PrintTransformer()
    modified_tree = tree.visit(transformer)
    return modified_tree.code


def get_all_python_files(target: Path) -> list:
    # get all python files except those in the venv directory
    pattern = "/[!venv]*.py"
    files = glob.glob(str(target) + pattern, recursive=True)
    return files


if __name__ == "__main__":
    typer.run(main)
