from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='MyTxtPdf',
    version='1.0.2',
    license='MIT License',
    author='Pedro Tércio ',
    long_description=readme,
    long_description_content_type="text/markdown",
    url = 'https://github.com/pedrotercio14/Pacote-InfoPdf.git',
    author_email='pedrotercio@gmail.com',
    keywords='pdf',
    description=u'Teste referente a pubiclação do pacote',
    packages=['MyTxtpdf'],
    install_requires=['pyttsx3', 'PyPDF2','pdfplumber', 'googletrans'], )