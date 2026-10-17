from pathlib import Path
from pdf2docx import Converter
import pandas as pd
from docx import Document
import pymupdf
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from rich.progress import track
from src.utils.logger import log

# Converter arquivo por arquivo 1 -> 1


def convert_document(input_path: str, output_path: str):
    inp = Path(input_path)
    out = Path(output_path)

    if not inp.exists():
        log.error(f"Arquivo de entrada não encontrado: {inp}")
        raise FileNotFoundError(f"O arquivo {inp} não existe!!")

    ext_in = inp.suffix.lower()
    ext_out = out.suffix.lower()

    log.info(
        f"Iniciar conversão de {ext_in.upper()} para {ext_out.upper()}...")
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        # 1: PDF -> Docx
        if ext_in == ".pdf" and ext_out == ".docx":
            cv = Converter(str(inp))
            cv.convert(str(out), start=0, end=None)
            cv.close()

        # 2: Docx -> PDF
        elif ext_in == ".docx" and ext_in == ".pdf":
            doc = Document(str(inp))
            pdf_doc = SimpleDocTemplate(str(out), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            for para in doc.paragraphs:
                if para.text.strip():
                    story.append(Paragraph(para.text, styles['Normal']))
            pdf_doc.build(story)

        # 3: Excel -> Docx
        elif ext_in in [".xlsx", "xls"] and ext_out == ".docx":
            df = pd.read_excel(str(inp))
            doc = Document()
            doc.add_heading(f"Relatório de {inp.name}", level=1)

            table = doc.add_table(rows=df.shape[0] + 1, cols=df.shape[1])
            for j, col_name in enumerate(df.columns):
                table.cell(0, j).text = str(col_name)
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    table.cell(i + 1, j).text = str(df.iat[i, j])
            doc.save(str(out))

        # 4: Excel -> PDF
        elif ext_in in [".xlsx", ".xls"] and ext_out == ".pdf":
            df = pd.read_excel(str(inp))
            pdf_doc = SimpleDocTemplate(str(out), pagesize=letter)
            story = []

            data = [list(df.columns)] + df.values.tolist()
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(t)
            pdf_doc.build(story)

        # 5: CSV -> Excel
        elif ext_in == ".csv" and ext_out in [".xlsx", ".xls"]:
            df = pd.read_csv(str(inp))
            df.to_excel(str(out), index=False)

        # PDF -> TXT
        elif ext_in == ".pdf" and ext_out == ".txt":
            doc_pymupdf = pymupdf.open(str(inp))
            text = ""
            for page in doc_pymupdf:
                text += page.get_text()
            out.write_text(text, encoding="utf-8")

        else:
            raise NotImplementedError(
                f"A conversão direta de {ext_in} para {ext_out} não é suportada.")

        log.success(f"Arquivo convertido com sucesso: {out}")

    except Exception as e:
        log.exception(
            f"Erro crítico durante a conversão do arquivo {inp.name}: {e}")
        raise e

# Converter varios arquivos ao mesmo tempo N <> N


def batch_convert(input_dir: str, output_dir: str, target_format: str):
    inp_dir = Path(input_dir)
    out_dir = Path(output_dir)

    if not inp_dir.is_dir():
        log.error(f"Diretório de entrada inválido: {inp_dir}")
        raise NotADirectoryError(
            f"O caminho {inp_dir} não é um diretório válido.")

    out_dir.mkdir(parents=True, exist_ok=True)
    target_ext = f".{target_format.lower().lstrip('.')}"

    files = [f for f in inp_dir.iterdir() if f.is_file()]
    if not files:
        log.warning(f"Nenhum arquivo encontrado no diretório: {inp_dir}")
        return

    log.info(
        f"Iniciar conversão em lote de {len(files)} arquivos para '{target_ext}'...")

    success_count = 0
    fail_count = 0

    for file_path in track(files, description="[cyan]A converter lote..."):
        ext_in = file_path.suffix.lower()
        if ext_in == target_ext:
            continue

        out_file_path = out_dir / f"{file_path.stem}{target_ext}"

        try:
            convert_document(str(file_path), str(out_file_path))
            success_count += 1
        except Exception:
            fail_count += 1
            log.error(
                f"Falha isolada no arquivo {file_path.name}. A continuar lote...")

    log.success(
        f"Lote concluído! Sucessos: {success_count} | Falhas: {fail_count}")
