import json
import os

import matplotlib.pyplot as plt
import pandas as pd


def ler_json_e_gerar_dataframe(caminho_arquivo: str) -> pd.DataFrame:
    """Lê um arquivo JSON com dados de ativos e gera um DataFrame."""

    # Campos desejados fixos
    campos = ["ativo", "classe", "tipo", "qtd", "valor"]

    try:
        with open(caminho_arquivo, "r") as file:
            # Carregar os dados do arquivo JSON
            dados = json.load(file)

        # Filtra os dados para selecionar apenas os campos desejados
        dados_filtrados = [
            {campo: ativo.get(campo) for campo in campos} for ativo in dados
        ]

        # Converter para DataFrame
        df = pd.DataFrame(dados_filtrados)

        # Calcular a coluna 'patrimonio' (produto de qtd * valor)
        df["patrimonio"] = df["qtd"] * df["valor"]

        return df

    except Exception as e:
        print(f"Erro ao ler o arquivo ou gerar o DataFrame: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


def ler_multipos_arquivos(caminhos_arquivos: list) -> pd.DataFrame:
    """Lê múltiplos arquivos JSON e retorna um DataFrame único."""
    dataframes = []

    for caminho in caminhos_arquivos:
        # Verifica se o arquivo existe
        if os.path.exists(caminho):
            df = ler_json_e_gerar_dataframe(caminho)
            if not df.empty:
                dataframes.append(df)
        else:
            print(f"Arquivo não encontrado: {caminho}")

    # Concatenar todos os DataFrames em um só
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    else:
        return (
            pd.DataFrame()
        )  # Retorna um DataFrame vazio se nenhum arquivo válido for lido


# Exemplo de como usar
if __name__ == "__main__":
    arquivos = [
        "data/acoes.json",
        "data/fiis.json",
        "data/pgbl.json",
        "data/rendafixa.json",
    ]  # Substitua pelos caminhos reais
    df = ler_multipos_arquivos(arquivos)

    # Calcular o patrimônio total
    patrimonio_total = df["patrimonio"].sum()
    print(patrimonio_total)

    # Calcular a porcentagem de cada ativo sobre o patrimônio total
    df["percentual"] = (df["patrimonio"] / patrimonio_total) * 100

    # Exibir o DataFrame
    if not df.empty:
        print(df)
    else:
        print("Erro ao gerar o DataFrame a partir dos arquivos.")

    #  1. Gráfico de rosca para 'classe' x 'patrimonio'
    classe_patrimonio = df.groupby("classe")["patrimonio"].sum()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        classe_patrimonio,
        labels=classe_patrimonio.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.4),
    )
    ax.set_title("Distribuição de Patrimônio por Classe")
    # plt.show()

    # 2. Gráfico de rosca para 'tipo' x 'patrimonio'
    tipo_patrimonio = df.groupby("tipo")["patrimonio"].sum()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        tipo_patrimonio,
        labels=tipo_patrimonio.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.4),
    )
    ax.set_title("Distribuição de Patrimônio por Tipo")
    plt.show()
