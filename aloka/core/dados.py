import pandas as pd

def carregar_csv(arquivo) -> pd.DataFrame:
    """Lê e retorna um DataFrame do arquivo CSV."""
    try:
        df = pd.read_csv(arquivo)
        df = limpar_colunas_valores(df)
        return df
    except Exception as e:
        raise ValueError(f"Erro ao carregar CSV: {e}")
    


def colunas_numericas(df: pd.DataFrame):
    """Retorna uma lista de colunas numéricas do DataFrame."""
    return df.select_dtypes(include=["float64", "int64"]).columns.tolist()

def calcular_media(df: pd.DataFrame, coluna: str):
    """Calcula a média de uma coluna numérica."""
    return df[coluna].mean()

def limpar_colunas_valores(df: pd.DataFrame) -> pd.DataFrame:
    """Converte strings formatadas como moeda brasileira para floats"""
    
    def converter(valor: str) -> float:
        if isinstance(valor, str):
            return float(
                valor.replace("R$", "")
                     .replace(".", "")
                     .replace(",", ".")
                     .strip()
            )
        return valor

    colunas_para_converter = ["Quantidade"]
    for col in colunas_para_converter:
        if col in df.columns:
            df[col] = df[col].apply(converter)
    
    return df
