import json
import time

import requests
import yfinance as yf


def atualizar_cotacoes_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for ativo in dados:
        ticker = ativo["ativo"]
       
        try:
            cotacao = get_price(ticker)
            print(cotacao)
            ativo["valor"] = round(float(cotacao), 2)
        except Exception as e:
            print(f"Erro ao buscar {ticker}: {e}")
            time.sleep(2)  # espere 2 segundos entre chamadas
            ativo["valor"] = None

    # sobrescreve o arquivo original
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print("Arquivo atualizado com os valores de cotação.")


def get_price(ticker) -> float | bool:
    """Fetches the current stock price using `info["currentPrice"]`."""

    try:
        # Retrieve stock data
        stock = yf.Ticker(ticker + ".SA")

        # Get current price
        price = stock.info.get("currentPrice")

        # Ensure the info dictionary is not None
        if price is not None:
            return price
        else:
            print("No data returned!")
            return False

    except Exception as e:
        # Log any exception that occurs
        print(f"Error fetching stock price for {ticker}: {e}")
    return None

# Exemplo de como usar
if __name__ == "__main__":

    preco = get_price("BBAS3")
    if preco is not None:
        print(f"Preço atual de BBAS3: R${preco:.2f}")
    else:
        print("Não foi possível obter o preço.")

    arquivos = ["data/acoes.json", "data/fiis.json"]

    for caminho_arquivo in arquivos:

        # Lê os dados principais do arquivo pgbl.json
        atualizar_cotacoes_arquivo(caminho_arquivo)
