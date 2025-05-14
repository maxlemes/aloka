import json
import time

import requests
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries as ts


def buscar_preco(codigo: str) -> float:
    """
    Busca o último preço de fechamento do ativo.

    Parâmetros:
        codigo (str): Ticker do ativo (ex: 'PETR4', 'AAPL', etc)

    Retorna:
        float: Preço de fechamento mais recente
    """
    # Se não tiver ponto, assumimos que é da B3
    if "." not in codigo:
        codigo += ".SA"

    try:
        ticker = yf.Ticker(codigo)
        historico = ticker.history(period="1d")
        if historico.empty:
            raise ValueError(f"Nenhum dado encontrado para {codigo}")
        return historico["Close"].iloc[-1]
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar preço de {codigo}: {e}")


def preco_formatado(codigo: str) -> str:
    try:
        preco = buscar_preco(codigo)
        return f"O preço atual de {codigo.upper()} é R$ {preco:.2f}"
    except Exception as e:
        return f"Erro ao buscar preço de {codigo}: {e}"


def atualizar_cotacoes_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for ativo in dados:
        ticker = ativo["ativo"]
        try:
            cotacao = get_price_brapi(ticker, token)
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
        print(stock)

        # Get current price
        price = stock.fast_info.get("lastPrice")

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


def get_price_brapi(ticker: str, token: str) -> float | None:
    """Busca o preço atual da ação via API da Brapi com token de autenticação."""
    try:
        url = f"https://brapi.dev/api/quote/{ticker}?range=1d&interval=1d"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])

        if results and "regularMarketPrice" in results[0]:
            return results[0]["regularMarketPrice"]
        else:
            print(f"[{ticker}] Dados ausentes ou malformados na resposta da Brapi.")
            return None
    except Exception as e:
        print(f"[{ticker}] Erro ao buscar preço na Brapi: {e}")
        return None


# Exemplo de como usar
if __name__ == "__main__":
    token = "pdqpd5oveyyKeRpwrJYSrT"
    preco = get_price_brapi("BBAS3", token)
    if preco is not None:
        print(f"Preço atual de BBAS3: R${preco:.2f}")
    else:
        print("Não foi possível obter o preço.")

    arquivos = ["data/acoes.json", "data/fiis.json"]

    for caminho_arquivo in arquivos:

        # Lê os dados principais do arquivo pgbl.json
        atualizar_cotacoes_arquivo(caminho_arquivo)
