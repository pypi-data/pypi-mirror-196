# Pacote-InfoPdf
Pacote Python desenvolvido na disciplina de Programação Orientada a Objetos II, com a funcionalidade de ler e traduzir arquivos em formato Pdf e fazer a conversão traduzida para TXT.

# Instalação

pip install MyTxtPdf

# Uso
from MyTxtPdf import MyTxtPdf

my_pdf = MyTxtPdf()
my_pdf.SayThis('arquivo.pdf')

my_pdf = MyTxtPdf()
my_pdf.Translator('meuarquivo.pdf', 1)
