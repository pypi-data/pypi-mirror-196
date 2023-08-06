from setuptools import setup
setup(
    name='MiPdf',
    version='0.0.1',
    description='Tradução de paginas e leitura de texto com voz do sistema',
    long_description='Realiza a tradução de uma página especifica de seu pdf e converte traduzida para ingles e é possivel leitura de um arquivo pdf com voz do sistema',
    author='Francisco Aparicio & Pedro Tercio',
    author_email='faparicionc@gmail.com',
    packages=['pooii-pacote'],
    python_requires='>=3.9',
    entry_points={'console_scripts' : ['meu-script = projeto.cli:cli']},
    install_requires=["poetry-core", "pyttsx3", "PyPDF2", "pdfplumber", "googletrans"]

)