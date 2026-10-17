# 📄 Convertit

> Um conversor de documentos robusto e profissional via Linha de Comando (CLI), desenvolvido em Python com foco em automação, processamento em lote e auditoria segura.

---

## 🚀 Sobre o Projeto

O **Convertit** nasceu para simplificar a conversão entre diferentes formatos de documentos do dia a dia (PDF, Word, Excel, CSV e Texto) de forma automatizada. Ele foi arquitetado seguindo padrões de mercado — incluindo estrutura modular (`src/`), gestão de dependências moderna (`pyproject.toml`), interface amigável via Typer com barras de progresso (`Rich`), e um sistema centralizado de auditoria (`Loguru`).

---

## ✨ Funcionalidades Principais

* **🔄 Conversão Individual e em Lote:** Converta um único arquivos ou diretórios inteiros com dezenas de documentos de uma só vez.
* **🛡️ Isolamento de Erros (Failsafe):** Em processamentos em lote, se um documento falhar ou estiver corrompido, o sistema regista o erro e continua o lote sem interromper a execução dos restantes arquivos.
* **📊 Feedback Visual:** Barras de progresso dinâmicas e mensagens coloridas no terminal através da biblioteca `Rich`.
* **📝 Auditoria Completa:** Registo detalhado de todas as operações e falhas num arquivos de log persistente (`logs/app.log`).

---

## 🔄 Formatos Suportados

| Formato de Entrada | Formatos de Destino Suportados |
| :--- | :--- |
| **PDF** (`.pdf`) | Word (`.docx`), Texto (`.txt`) |
| **Word** (`.docx`) | PDF (`.pdf`) |
| **Excel** (`.xlsx`, `.xls`) | CSV (`.csv`), Word (`.docx`), PDF (`.pdf`) |
| **CSV** (`.csv`) | Excel (`.xlsx`) |

---

## 🛠️ Tecnologias Utilizadas

* **[Typer]**: Construção da interface de linha de comando (CLI).
* **[Rich]**: Formatação visual e barras de progresso.
* **[Loguru]**: Sistema de logs assíncrono e simplificado.
* **[Pandas]**: Processamento de dados e motores de leitura de arquivoss.
* **[Pytest]**: Suite de testes unitários.

---

## 📦 Instalação

Certifique-se de que tem o Python 3.8+ instalado no seu sistema. Siga os passos abaixo para configurar o ambiente local:

1. **Clone o repositório:**
```bash
   git clone https://github.com/elsantosdev/convertit.git
