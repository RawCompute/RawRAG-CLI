
from rich import spinner
from rich.markdown import Markdown
from rich.panel import Panel
import typer
import pyfiglet
from rich.console import Console
import os
import pathlib
import requests

from rawrag_cli.core.chunker import chunk_text
from rawrag_cli.core.database import get_chunks, insert_chunk
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
            chunks = chunk_text(text, chunk_size, chunk_overlap) 

            for chunk in chunks:
                vector = get_embedding(chunk)
                vector_store.add_vector(vector)
                insert_chunk(str(path), chunk)

        vector_store.save_index()

    console.print(f"[bold green]✔ Successfully indexed {len(filepaths)} files![/bold green]")      
    
@app.command()
def query(question: str):
    print_header()

    with console.status("[bold yellow]Processing your query...[/bold yellow]", spinner="bouncingBar"):
        query_vector = get_embedding(question)
        vector_store = VectorMath()

        top_indices = vector_store.search(query_vector, top_k=3)
        if not top_indices:
            console.print("[bold red]No relevant chunks found for the query. Run [bold cyan]index[/bold cyan] first.[/bold red]")
            raise typer.Exit(code=1)
        chunk_ids = [int(index) + 1 for index in top_indices]
        chunks = get_chunks(chunk_ids)
        if not chunks:
            console.print("[bold red]No matching chunks found in the database. Run [bold cyan]index[/bold cyan] first.[/bold red]")
            raise typer.Exit(code=1)

        context_string = "\n\n".join(chunks)

        prompt = f"""You are a helpful coding assistant answering questions about a local codebase.
        Use ONLY the provided codebase context below to answer the user's question. If the answer is not in the context, say you don't know.

        Codebase Context:
        {context_string}

        Question: {question}
        Answer:"""

        url = OLLAMA_URL
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            answer = response.json().get("response", "No response received.")
        
            console.print(Panel(Markdown(answer), title="[bold green]RawRAG Answer[/bold green]", border_style="green"))

        except requests.exceptions.ConnectionError:
            console.print("[bold red]Error:[/bold red] Could not connect to Ollama. Make sure Ollama is running in the background (`ollama serve`).")
            raise typer.Exit(code=1)
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]API Error:[/bold red] {e}")
            raise typer.Exit(code=1)


# Rag-logic

def main() -> None:
    app()

if __name__ == "__main__":
    main()
