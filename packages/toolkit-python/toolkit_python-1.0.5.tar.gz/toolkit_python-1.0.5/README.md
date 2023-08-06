## INSTRUÇÕES

---

### Configuração Inicial

---

1.  Faça o git clone deste repositório
2.  Crie um ambiente virtual do python instalando:

    `python -m venv ./venv`

3.  Após a criação do ambiente, sera necessário ativar o ambiente virtual:

    `venv\Scripts\activate`

## Configuração do Pacote

---

1. Upgrade setuptools

   `python -m pip install --user --upgrade setuptools`

2. Generate your source distribution

   `python setup.py sdist`

3. Install local development mode

   `pip install -e C:\RF\Desenv\toolkit-python`

   - Configure settings VSCode resolved Pylance reportMissingImports

     `"python.analysis.extraPaths": ["C:\\RF\\Desenv\\toolkit-python"]`
