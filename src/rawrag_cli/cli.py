import typer
import pyfiglet
from rich.console import Console

app = typer.Typer()
console = Console()

def print_header():
    ascii_art = pyfiglet.figlet_format("RawRAG", font="larry3d")
    console.print(ascii_art, style="bold #D97757")

@app.command()
def query(question: str):
    print_header()
    console.print(f"Searching local vector database for: [cyan]{question}[/cyan]")

# Rag-logic

def main() -> None:
    app()


if __name__ == "__main__":
    main()
