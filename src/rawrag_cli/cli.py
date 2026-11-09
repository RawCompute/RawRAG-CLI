import typer
import pyfiglet
from rich.console import Console
import os
import pathlib

from .core.chunker import chunk_text
from .core.vector import VectorMath
from .core.config import chunk_size, chunk_overlap, OLLAMA_URL, DB_PATH
from .core.embeddings import get_embedding

app = typer.Typer()
console = Console()

def print_header():
    ascii_art = pyfiglet.figlet_format("RawRAG CLI", font="ansi_shadow")
    console.print(ascii_art, style="bold #D97757")

@app.command()
def index(directory: str):
    console.print(f"Indexing files in directory: [cyan]{directory}[/cyan]")
    for file_path in pathlib.Path(directory).rglob("*"):
        pass
    
@app.command()
def query(question: str):
    print_header()
    console.print(f"Searching local vector database for: [cyan]{question}[/cyan]")

# Rag-logic

def main() -> None:
    app()


if __name__ == "__main__":
    main()
