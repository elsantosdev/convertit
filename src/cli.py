import warnings
from pathlib import Path
import typer
from src.converters.handler import convert_document, batch_convert
from src.utils.logger import log

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = typer.Typer(
    help="Convertit - Conversor profissional de documentos via CLI.",
    add_completion=False
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    input_path: str = typer.Option(..., "--input", "-i",
                                   help="Caminho do arquivo ou diretório de entrada."),
    output_path: str = typer.Option(..., "--output", "-o",
                                    help="Caminho do arquivo ou diretório de saída."),
    to_format: str = typer.Option(
        None, "--to", "-t", help="Formato de destino para conversão em lote (ex: docx, pdf, txt, csv, xlsx).")
):
    """
    Converte arquicos individuais ou pastas inteiras de forma automática e segura.
    """
    if ctx.invoked_subcommand is not None:
        return

    inp = Path(input_path)

    try:
        if inp.is_dir():
            if not to_format:
                typer.echo(typer.style(
                    "✖ Erro: O parâmetro --to (-t) é obrigatório para conversão em lote de diretórios.", fg=typer.colors.RED, bold=True))
                raise typer.Exit(code=1)

            log.info(
                f"Modo Lote detetado: {input_path} -> {output_path} (Destino: {to_format})")
            batch_convert(input_path, output_path, to_format)
            typer.echo(typer.style(
                "✔ Conversão em lote concluída! Verifique os logs para detalhes.", fg=typer.colors.GREEN, bold=True))

        elif inp.is_file():
            log.info(
                f"Modo Individual detetado: {input_path} -> {output_path}")
            convert_document(input_path, output_path)
            typer.echo(typer.style("✔ Conversão concluída com sucesso!",
                       fg=typer.colors.GREEN, bold=True))

        else:
            raise FileNotFoundError(
                f"O caminho de entrada não existe: {input_path}")

    except Exception as e:
        log.exception(f"Erro na execução da CLI: {e}")
        typer.echo(typer.style(
            "✖ Falha na operação. Verifique os logs em logs/app.log para detalhes.", fg=typer.colors.RED, bold=True))
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
