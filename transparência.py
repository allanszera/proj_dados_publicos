import pandas as pd
import requests
from io import BytesIO, StringIO
from zipfile import ZipFile
import chardet

url = 'https://www.transparencia.df.gov.br/arquivos/Remuneracao_2024.zip'

resposta = requests.get(url)
resposta.raise_for_status()

zip = BytesIO(resposta.content)

# Nome do arquivo que você quer abrir
arquivo_desejado = "Remuneracao_2024/Remuneracao_2024_09.csv"

zip_data = BytesIO(resposta.content)

# Abrindo o arquivo ZIP
with ZipFile(zip_data) as zip_file:
    # Verifica se o arquivo existe no ZIP
    if arquivo_desejado in zip_file.namelist():
        print(f"Abrindo o arquivo: {arquivo_desejado}")
        with zip_file.open(arquivo_desejado) as arquivo:
            # Lendo o conteúdo do arquivo
            conteudo = arquivo.read()

            # Decodificando como ISO-8859-1 (com base em informações anteriores)
            try:
                texto = conteudo.decode("ISO-8859-1")
                print(f"\nConteúdo do arquivo '{arquivo_desejado}':\n")
                print(texto[:500])  # Mostra os primeiros 500 caracteres para evitar sobrecarga
            except Exception as e:
                print(f"Erro ao decodificar o arquivo '{arquivo_desejado}': {e}")
    else:
        print(f"O arquivo '{arquivo_desejado}' não foi encontrado no ZIP.")
        
# Corrigir linhas problemáticas ao carregar o DataFrame
texto = pd.read_csv(StringIO(texto), delimiter=";", on_bad_lines="skip")

# Limpar a coluna "LÍQUIDO"
if "LÍQUIDO" in texto.columns:
    texto["LÍQUIDO"] = (
        texto["LÍQUIDO"]
        .astype(str)
        .str.replace("R\$", "", regex=True)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    texto["LÍQUIDO"] = pd.to_numeric(texto["LÍQUIDO"], errors="coerce")

    # Verificar novamente
    max_liquido = texto["LÍQUIDO"].max()
    print(f"\nMaior valor LÍQUIDO: {max_liquido}")

    # Linha associada ao maior valor
    linha_max_liquido = texto[texto["LÍQUIDO"] == max_liquido]
    print("\nDetalhes da linha com o maior valor LÍQUIDO:")
    print(linha_max_liquido)
else:
    print("A coluna 'LÍQUIDO' não foi encontrada no arquivo CSV.")