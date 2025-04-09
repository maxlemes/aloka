from aloka.core.precos import preco_formatado


if __name__ == "__main__":
    # Teste no terminal
    ativos = ["PETR4", "LEVE3", "VALE3", "TUPY3"]
    for ativo in ativos:
        print(preco_formatado(ativo))

