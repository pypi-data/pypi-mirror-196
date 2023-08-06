import pyttsx3
import PyPDF2
import pdfplumber as pdftool
from googletrans import Translator
 

class MyTxtPdf:

    """
    Classe responsável por ler e traduzir um arquivo PDF em texto e áudio.

    Parâmetros:
    ----------
    Nenhum

    Métodos:
    -------
    __init__(self):
        Inicializa a classe.

    SayThis(self, nome_pdf):
        Lê o conteúdo de um arquivo PDF e o reproduz em áudio usando a biblioteca pyttsx3.

        Parâmetros:
        ----------
        nome_pdf: str
            O nome do arquivo PDF a ser lido.

        Retorno:
        -------
        Nenhum.

    Translator(self, nome_pdf, pagina):
        Traduz o conteúdo de uma página específica de um arquivo PDF para inglês e salva em um arquivo de texto.

        Parâmetros:
        ----------
        nome_pdf: str
            O nome do arquivo PDF a ser traduzido.
        pagina: int
            O número da página a ser traduzida.

        Retorno:
        -------
        Nenhum.
    """

    def __init__(self):
        """
        Inicializa a classe.
        """
        pass

    def SayThis(self, nome_pdf):
        """
        Lê o conteúdo de um arquivo PDF e o reproduz em áudio usando a biblioteca pyttsx3.

        Parâmetros:
        ----------
        nome_pdf: str
            O nome do arquivo PDF a ser lido.

        Retorno:
        -------
        Nenhum.
        """

        txt = ''
        with pdftool.open(nome_pdf) as tool:

            for p_no, pagina in enumerate(tool.pages, 1):

                pag = f'\nPAGINA {p_no}\n'

                data = pagina.extract_text()

                txt += pag
                txt += data
        engine = pyttsx3.init()
        engine.say(txt)
        engine.runAndWait()

    def Translator(self, nome_pdf, pagina):
        """
        Traduz o conteúdo de uma página específica de um arquivo PDF para inglês e salva em um arquivo de texto.

        Parâmetros:
        ----------
        nome_pdf: str
            O nome do arquivo PDF a ser traduzido.
        pagina: int
            O número da página a ser traduzida.

        Retorno:
        -------
        Nenhum.
        """

        with pdftool.open(nome_pdf) as pdf:
            page = pdf.pages[pagina-1]
            content = page.extract_text()
            
        arquivo = open('arquivo.txt', 'w', encoding='utf-8')
        translator = Translator(service_urls=['translate.google.com'])

        traducao = translator.translate(content, dest='en').text

        arquivo.write(traducao)
        arquivo.close()

MyTxtPdf = MyTxtPdf()
MyTxtPdf.SayThis('certificado.pdf')

MyTxtPdf= MyTxtPdf()
MyTxtPdf.Translator('certificado.pdf', 1)


