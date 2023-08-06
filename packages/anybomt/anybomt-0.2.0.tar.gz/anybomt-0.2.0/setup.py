from setuptools import setup

# Leitura do arquivo README.md
with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Configuração do pacote
setup(
    name='anybomt',
    version='0.2.0',
    license='MIT',
    author='AnyBoMath',
    author_email='bidjorys@gmail.com',
    description='Uma biblioteca para facilitar sua jornada em matemática',
    long_description=long_description,
    long_description_content_type='text/markdown',
  # Substitua com o link do seu repositório no GitHub
    packages=[''],  # Lista de pacotes que serão incluídos
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
