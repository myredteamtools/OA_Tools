from rich.console import Console

def custom_print(message: str, header: str) -> None:
    console: Console = Console()
    header_colors: dict = {"+": "green", "-": "red", "!": "yellow", "*": "blue"}
    console.print(
        f"[bold {header_colors.get(header, 'white')}][{header}][/bold {header_colors.get(header, 'white')}] {message}"
    )