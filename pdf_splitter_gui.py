import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import sys
from pypdf import PdfReader, PdfWriter

def get_downloads_path():
    """Tenta obter o caminho da pasta Downloads de forma multiplataforma."""
    if sys.platform == 'win32':
        # Para Windows
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
                downloads_path = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
                return downloads_path
        except Exception:
            # Fallback para o diretório inicial
            return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        # Para Linux/macOS
        return os.path.join(os.path.expanduser('~'), 'Downloads')

class PDFSplitterApp:
    def __init__(self, master):
        self.master = master
        master.title("Separador de Páginas PDF")

        # Configuração do estilo (usando ttk)
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' ou 'alt' ou 'default'

        # Variáveis de controle
        self.pdf_filepath = tk.StringVar()
        self.pdf_filepath.set("Nenhum arquivo selecionado")

        # Configuração do caminho de saída
        self.downloads_path = get_downloads_path()
        self.output_dir = os.path.join(self.downloads_path, "PDFs_Separados")

        # Frames
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill='both', expand=True)

        # 1. Seleção do Arquivo
        file_frame = ttk.LabelFrame(main_frame, text="1. Selecione o Arquivo PDF", padding="10")
        file_frame.pack(fill='x', pady=10)

        self.label_file = ttk.Label(file_frame, textvariable=self.pdf_filepath, wraplength=400)
        self.label_file.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        self.btn_select = ttk.Button(file_frame, text="Abrir PDF", command=self.select_pdf)
        self.btn_select.pack(side='right', padx=5, pady=5)

        # 2. Informações
        info_frame = ttk.LabelFrame(main_frame, text="2. Detalhes", padding="10")
        info_frame.pack(fill='x', pady=10)

        self.label_pages = ttk.Label(info_frame, text="Páginas encontradas: 0")
        self.label_pages.pack(anchor='w', pady=2)

        self.label_output = ttk.Label(info_frame, text=f"Saída: {self.output_dir}")
        self.label_output.pack(anchor='w', pady=2)

        # 3. Processamento
        process_frame = ttk.Frame(main_frame, padding="10")
        process_frame.pack(fill='x', pady=10)

        self.btn_process = ttk.Button(process_frame, text="Separar Páginas", command=self.split_pdf, state=tk.DISABLED)
        self.btn_process.pack(fill='x')

        # Status Bar
        self.status_bar = ttk.Label(master, text="Pronto para começar.", relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(fill='x', side=tk.BOTTOM, ipady=2)

    def select_pdf(self):
        """Abre a caixa de diálogo para selecionar o arquivo PDF."""
        filepath = filedialog.askopenfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if filepath:
            self.pdf_filepath.set(filepath)
            self.btn_process.config(state=tk.NORMAL)
            self.count_pages(filepath)
            self.status_bar.config(text=f"PDF selecionado: {os.path.basename(filepath)}")
        else:
            self.pdf_filepath.set("Nenhum arquivo selecionado")
            self.btn_process.config(state=tk.DISABLED)
            self.label_pages.config(text="Páginas encontradas: 0")
            self.status_bar.config(text="Seleção de arquivo cancelada.")

    def count_pages(self, filepath):
        """Conta o número de páginas do PDF e atualiza a interface."""
        try:
            reader = PdfReader(filepath)
            num_pages = len(reader.pages)
            self.label_pages.config(text=f"Páginas encontradas: {num_pages}")
            self.master.num_pages = num_pages
        except Exception as e:
            self.label_pages.config(text="Páginas encontradas: Erro")
            messagebox.showerror("Erro ao ler PDF", f"Não foi possível ler o arquivo PDF: {e}")
            self.btn_process.config(state=tk.DISABLED)

    def split_pdf(self):
        """Logica para separar o PDF em arquivos de uma página."""
        input_path = self.pdf_filepath.get()

        if not os.path.exists(input_path):
            messagebox.showerror("Erro", "Arquivo PDF não encontrado.")
            return

        # Garante que o diretório de saída exista
        os.makedirs(self.output_dir, exist_ok=True)

        try:
            self.status_bar.config(text="Iniciando a separação...")
            self.master.update() # Força a atualização da interface

            # Leitor e nome base
            reader = PdfReader(input_path)
            
            # Obtém o nome do arquivo sem a extensão para usar como prefixo
            base_filename = os.path.splitext(os.path.basename(input_path))[0]
            
            total_pages = len(reader.pages)
            
            for i, page in enumerate(reader.pages):
                page_num = i + 1
                
                # Cria um novo escritor para cada página
                writer = PdfWriter()
                writer.add_page(page)

                # Nome do arquivo de saída: Ex: Texte1.pdf, Texte2.pdf, etc.
                output_filename = f"{base_filename}{page_num}.pdf"
                output_path = os.path.join(self.output_dir, output_filename)

                # Salva o novo PDF
                with open(output_path, "wb") as outputStream:
                    writer.write(outputStream)

                self.status_bar.config(text=f"Processando página {page_num} de {total_pages}...")
                self.master.update()

            messagebox.showinfo("Sucesso!", 
                                f"O PDF foi separado em {total_pages} arquivos.\n\nSalvos em: {self.output_dir}")
            self.status_bar.config(text="Processamento concluído com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro de Processamento", f"Ocorreu um erro durante a separação: {e}")
            self.status_bar.config(text="Processamento falhou.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
