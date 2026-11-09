
from rich import spinner
import typer
import pyfiglet
from rich.console import Console
import os
import pathlib

from rawrag_cli.core.chunker import chunk_text
from rawrag_cli.core.database import insert_chunk
from rawrag_cli.core.vector import VectorMath
from rawrag_cli.core.config import chunk_size, chunk_overlap, OLLAMA_URL, DB_PATH
from rawrag_cli.core.embeddings import get_embedding

app = typer.Typer()
console = Console()

def print_header():
    ascii_art = pyfiglet.figlet_format("RawRAG CLI", font="ansi_shadow")
    console.print(ascii_art, style="bold #D97757")

@app.command()
def index(directory: str = typer.Argument(".", help="Path to database")):
    print_header()
    console.print(f"Indexing files in directory: [cyan]{directory}[/cyan]")

    # Initializing the database table BEFORE the loop (debugging)
    from .core.database import initialize_database
    initialize_database()  

    with console.status("[bold yellow]Chunking and embedding files (this might take a minute)...[/bold yellow]", spinner="bouncingBar"):
        filepaths = list(pathlib.Path(directory).rglob("*.py"))

        if not filepaths:
            console.print("[bold red]No .py files found in the specified directory.[/bold red]")
            raise typer.Exit(code=1)

        vector_store = VectorMath()

        for path in filepaths:
            # Temporarily removed try/except to expose the exact error line
            text = path.read_text(encoding="utf-8")
            chunks = chunk_text(text, chunk_size=500, overlap=50) # Passed hardcoded ints just in case

            for chunk in chunks:
                vector = get_embedding(chunk)
                vector_store.add_vector(vector)
                insert_chunk(str(path), chunk)

        vector_store.save_index()

    console.print(f"[bold green]✔ Successfully indexed {len(filepaths)} files![/bold green]")      
    
@app.command()
def query(question: str):
    print_header()
    console.print(f"Searching local vector database for: [cyan]{question}[/cyan]")

# Rag-logic

def main() -> None:
    app()


if __name__ == "__main__":
    main()
