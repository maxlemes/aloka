
import os
import sys

# Adiciona a raiz do projeto ao sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd

from aloka.core.precos import preco_formatado
from aloka.core.dados import carregar_csv, colunas_numericas, calcular_media



def main():
    st.set_page_config(page_title="Aloka", layout="wide")
    st.title("💸 Aloka 💰 – Alocação Finaceira")


    arquivo = st.file_uploader("🔼 Envie seu arquivo CSV", type="csv")

    if arquivo is not None:
        try:
            df = carregar_csv(arquivo)

            st.subheader("📋 Visualização dos dados")
            st.dataframe(df)

            colunas = colunas_numericas(df)
            if colunas:
                coluna = st.selectbox("Selecione uma coluna para análise", colunas)
                media = calcular_media(df, coluna)
                st.metric(f"Média de {coluna}", f"{media:,.2f}")
                st.bar_chart(df[coluna])
            else:
                st.warning("Nenhuma coluna numérica disponível.")

        except ValueError as e:
            st.error(str(e))
    else:
        st.info("Envie um arquivo CSV para começar.")

    ativo = st.text_input("Digite o código do ativo", "PETR4")

    if ativo:
        resultado = preco_formatado(ativo)
        if resultado.startswith("Erro"):
            st.error(resultado)
        else:
            st.success(resultado)


if __name__ == "__main__":
    main()