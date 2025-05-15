import json
import os
import time
from datetime import datetime

import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def capturar_dados_fundo(link: str):

    # determina a URL geral
    url = f"https://statusinvest.com.br/fundos-de-investimento/{link}"

    # determina o XPATH das tabelas
    xpath_nome = "/html/body/main/header/div[2]/div/div[1]/h1"
    xpath_cota = "/html/body/main/div[2]/div/div/div[6]/div/div/strong"
    xpath_cnpj = "/html/body/main/div[4]/div/div[1]/div/div/div[1]/h5[2]"

    # inicia o navegador
    driver.get(url)

    # Aguarda carregar
    time.sleep(5)

    # captura os dados de interesse: nome, cota, cnpj
    try:
        nome = driver.find_element(By.XPATH, xpath_nome).text
    except Exception:
        print(f"Erro ao buscar nome do fundo: {link}")
        nome = "Desconhecido"

    try:
        cota = driver.find_element(By.XPATH, xpath_cota).text
        cota = float(cota.replace(",", "."))
    except Exception:
        print(f"Erro ao buscar cota do fundo: {link}")
        cota = None

    try:
        cnpj = driver.find_element(By.XPATH, xpath_cnpj).text
    except Exception:
        print(f"Erro ao buscar CNPJ do fundo: {link}")
        cnpj = "Não encontrado"

    dados = {"link": link, "nome": nome, "cnpj": cnpj, "valor": cota}

    # Cria a pasta 'data' se não existir
    os.makedirs("data", exist_ok=True)

    # Caminho do arquivo JSON
    caminho_arquivo = os.path.join("data", f"{link}.json")

    # Salva os dados em formato JSON
    salvar_json(dados, caminho_arquivo)


def atualizar_cotas(dados_principais, pasta="data"):
    # Caminho para o diretório onde os arquivos JSON estão armazenados
    for ativo in dados_principais:

        # Verifica se o link existe
        if ativo["link"]:

            # seleciona o arquivo JSON
            arquivo_json = os.path.join(pasta, f"{ativo['link']}.json")

            # # Verifica se o arquivo existe
            # if os.path.exists(arquivo_json):

            # Abre o arquivo do fundo
            dados_atuais = ler_json(arquivo_json)

            # Pega o valor de cota e adiciona ao dado principal
            ativo["valor"] = dados_atuais.get("valor")

            # adicionando a data da ultima atualizacao
            ativo["ultima_atualizacao"] = datetime.today().strftime("%d/%m/%Y %H:%M")

        else:
            print(f"O ativo {ativo['ativo']} não atualiza o preço.")

    return dados_principais


def ler_json(caminho_arquivo):
    """Lê e retorna dados de um arquivo JSON."""
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print(f"[ERRO] Arquivo não encontrado: {caminho_arquivo}")
        return []  # ou None, dependendo do contexto


def salvar_json(dados, caminho_arquivo):
    """Salva dados em um arquivo JSON com indentação e UTF-8."""
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"✔ Arquivo salvo: {caminho_arquivo}")


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


def atualizar_cotacoes(caminho_arquivo):

    # le o arquivo JSON
    dados = ler_json(caminho_arquivo)

    # para cata ativo no arquivo JSON captura a cotacao atual
    for ativo in dados:
        ticker = ativo["ativo"]

        try:
            cotacao = get_price(ticker)
            if cotacao:
                ativo["valor"] = round(float(cotacao), 2)
                ativo["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            else:
                ativo["valor"] = None

        except Exception as e:
            print(f"Erro ao buscar {ticker}: {e}")
            time.sleep(2)  # espere 2 segundos entre chamadas
            ativo["valor"] = None

    # sobrescreve o arquivo original
    salvar_json(dados, caminho_arquivo)

    print("✔ Arquivo atualizado com os valores de cotação.")


# Exemplo de como usar
if __name__ == "__main__":

    # definindo o endereço dos arquivos com os dados dos ativos
    classe_fundos = ["data/rendafixa.json", "data/pgbl.json"]
    classe_b3 = ["data/acoes.json", "data/fiis.json"]

    # criando uma lista vazia para os fundos
    fundos = []

    # lendo os links dos fundos
    for arquivo in classe_fundos:
        classe = ler_json(arquivo)

        for ativo in classe:
            link = ativo.get("link")
            if link:
                fundos.append(link)

    # # Configura o Firefox em modo headless (sem abrir a janela)
    # options = Options()
    # options.add_argument("--headless")
    # driver = webdriver.Firefox(options=options)

    # # Captura os dados de todos os fundos
    # for fundo in fundos:
    #     capturar_dados_fundo(fundo)
    #     # os.remove(f"data/{fundo}.json")

    # # fechando o navegador
    # driver.quit()

    print("Vamos agora capturar as cotações")

    # adicionando as informações dos fundos
    for classe_arquivo in classe_fundos:

        # Lê os dados principais do arquivo pgbl.json
        dados_classe = ler_json(classe_arquivo)

        # Atualiza os dados principais com o valor de cota
        dados_atualizados = atualizar_cotas(dados_classe)

        # Salva os dados atualizados no arquivo
        salvar_json(dados_atualizados, classe_arquivo)

    # adicionando as cotacoes dos ativos da B3
    for caminho_arquivo in classe_b3:

        # Lê os dados principais do arquivo pgbl.json
        atualizar_cotacoes(caminho_arquivo)
