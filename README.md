Markdown

# 📄 Separador de Páginas PDF com Interface Gráfica

Um utilitário simples em Python com interface gráfica (GUI) usando `tkinter` e a biblioteca `pypdf` para automatizar a divisão de arquivos PDF multipágina em documentos de página única.

Ideal para quem precisa rapidamente separar um grande PDF em seus componentes individuais, nomeados em ordem.

## ✨ Funcionalidades

* **Seleção Fácil:** Interface gráfica intuitiva para selecionar o arquivo PDF de entrada.
* **Contagem de Páginas:** Exibe o número total de páginas do documento selecionado.
* **Separação Automática:** Divide o PDF de entrada, criando um novo arquivo PDF para cada página.
* **Nomenclatura Inteligente:** Os arquivos de saída são nomeados sequencialmente (ex: `NomeDoArquivo1.pdf`, `NomeDoArquivo2.pdf`, etc.).
* **Organização:** Salva todos os arquivos de saída em uma pasta dedicada (`PDFs_Separados`) dentro do seu diretório `Downloads`.

## ⚙️ Pré-requisitos

Para executar este script, você precisará ter o Python instalado (versão 3.x recomendada).

Além disso, é necessário instalar a biblioteca `pypdf`:

```bash
pip install pypdf
```
🚀 Como Usar
1. Clonar o Repositório
Baixe ou clone este repositório para sua máquina local:
```Bash

git clone(https://github.com/Kaneka4850/Separador-de-pdf)
cd Separador-de-pdf

```
2. Executar o Script
Execute o arquivo Python para abrir a interface gráfica:

```Bash

python pdf_splitter_gui.py
```
3. Usando a Interface
Clique em "Abrir PDF": Selecione o arquivo PDF que você deseja dividir.

Verifique os Detalhes: O programa exibirá o número de páginas encontradas.

Clique em "Separar Páginas": Inicie o processo de divisão.

Conclusão: Uma mensagem de sucesso aparecerá ao término.

📁 Onde os Arquivos são Salvos?
Todos os PDFs de página única serão salvos no seguinte diretório:

[Sua Pasta de Usuário]/Downloads/PDFs_Separados/
💻 Estrutura do Projeto
O projeto é composto por um único arquivo principal:

.
└── pdf_splitter_gui.py  # Script principal com a lógica Tkinter e pypdf
