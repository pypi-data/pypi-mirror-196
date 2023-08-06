from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='PdfD',
    version='0.0.1',
    license='MIT License',
    author='Francisco Aparicio & Pedro Tercio',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='aparicionascimento111@gmail.com',
    keywords='Pdf',
    description=u'Traduzir paginas de um pdf e leitura do arquivo com voz do sistema',
    packages=['secundaria'],
    install_requires=["requests", "pyttsx3", "PyPDF2", "pdfplumber", "googletrans"],)