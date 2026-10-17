import pytest
from pathlib import Path
from src.converters.handler import convert_document


def test_convert_document_not_found():
    fake_input = "arquivo_teste.pdf"
    fake_output = "saida_teste.docx"

    with pytest.raises(FileNotFoundError):
        convert_document(fake_input, fake_output)


def test_unsupported_conversion_raises_error(tmp_path: Path):
    inp = tmp_path / "teste.xyz"
    out = tmp_path / "teste.abc"
    inp.write_text("dados falsos")

    with pytest.raises(NotImplementedError):
        convert_document(str(inp), str(out))
