import yfinance as yf


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
