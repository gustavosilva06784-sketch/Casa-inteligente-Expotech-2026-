"""Resumo das tarefas exportadas do Bubble.

Uso:
    python analise_tarefas.py                      (lê tarefas_bubble_export.csv)
    python analise_tarefas.py outro_arquivo.csv
    python analise_tarefas.py arquivo.csv --hoje 2026-11-09   (para testar com outra data)

Aceita as colunas do Bubble (nome, prazo, status, prioridade, responsavel,
email_responsavel) e também os nomes antigos (Nome da Tarefa, Data de Vencimento...).
"""
import argparse
import sys
import unicodedata

import warnings

import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)

# Evita erro de acentos/emojis em terminais Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Nome interno -> nomes aceitos no CSV (já sem acento e em minúsculas)
COLUNAS = {
    "id": ["id", "unique id"],
    "nome": ["nome", "nome da tarefa"],
    "prazo": ["prazo", "data de vencimento"],
    "status": ["status"],
    "prioridade": ["prioridade"],
}
OBRIGATORIAS = ["nome", "prazo", "status"]


def normalizar(texto):
    """Minúsculas e sem acento (compara 'Concluída' com 'concluida')."""
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return texto.strip().lower()


def padronizar_colunas(df):
    """Renomeia as colunas do CSV para os nomes internos."""
    mapa = {}
    for coluna in df.columns:
        for interno, aceitos in COLUNAS.items():
            if normalizar(coluna) in aceitos and interno not in mapa.values():
                mapa[coluna] = interno
    df = df.rename(columns=mapa)
    faltando = [c for c in OBRIGATORIAS if c not in df.columns]
    if faltando:
        sys.exit(
            "Erro: faltam colunas no CSV: " + ", ".join(faltando)
            + "\nColunas encontradas: " + ", ".join(map(str, df.columns))
        )
    return df


def calcular_urgencia(prazo, hoje):
    """Urgência pelo prazo (a prioridade escolhida no app fica na coluna 'prioridade')."""
    if pd.isnull(prazo):
        return "Baixa"
    dias = (prazo - hoje).days
    if dias < 0:
        return "Crítica (Atrasada)"
    if dias <= 2:
        return "Alta"
    if dias <= 7:
        return "Média"
    return "Baixa"


def analisar_tarefas(caminho_csv, data_hoje=None):
    # 1. Carregar o CSV
    try:
        df = pd.read_csv(caminho_csv, encoding="utf-8-sig", sep=None, engine="python")
    except FileNotFoundError:
        sys.exit(f"Erro: O arquivo '{caminho_csv}' não foi encontrado na pasta.")
    except pd.errors.EmptyDataError:
        sys.exit("Erro: o arquivo CSV está vazio.")

    df = padronizar_colunas(df)

    # 2. Converter a data (só o dia, sem hora, para 'vence hoje' não virar atraso)
    df["prazo"] = pd.to_datetime(df["prazo"], errors="coerce")
    if getattr(df["prazo"].dt, "tz", None) is not None:
        df["prazo"] = df["prazo"].dt.tz_localize(None)
    df["prazo"] = df["prazo"].dt.normalize()

    # 3. Remover tarefas concluídas
    df = df[df["status"].map(normalizar) != "concluida"].copy()

    hoje = pd.Timestamp(data_hoje).normalize() if data_hoje else pd.Timestamp.now().normalize()
    fim_semana = hoje + pd.Timedelta(days=6 - hoje.weekday())  # domingo

    # 4. Cálculo das tarefas atrasadas e da semana
    atrasadas = df[df["prazo"] < hoje]
    para_esta_semana = df[(df["prazo"] >= hoje) & (df["prazo"] <= fim_semana)]
    df["urgencia"] = df["prazo"].map(lambda p: calcular_urgencia(p, hoje))

    # 5. Exibição
    print("=" * 50)
    print("               RESUMO DAS TAREFAS              ")
    print(f"               Data: {hoje.strftime('%d/%m/%Y')}")
    print("=" * 50)
    print(f"📌 Tarefas atrasadas: {len(atrasadas)}")
    print(f"📌 Tarefas para esta semana: {len(para_esta_semana)}")
    print(f"📌 Total de tarefas pendentes: {len(df)}")
    print("-" * 50)

    if df.empty:
        print("Nenhuma tarefa pendente. Tudo em dia!")
        print("=" * 50)
        return

    print("\nDetalhamento por urgência (calculada pelo prazo):")
    print(df["urgencia"].value_counts().to_string())

    print("\nPróximas tarefas a vencer:")
    colunas = [c for c in ["id", "nome", "prazo", "prioridade", "urgencia"] if c in df.columns]
    saida = df.sort_values(by="prazo")[colunas].copy()
    saida["prazo"] = saida["prazo"].dt.strftime("%d/%m/%Y").fillna("sem prazo")
    saida = saida.rename(columns={"prioridade": "prioridade (app)", "urgencia": "urgência (prazo)"})
    print(saida.to_string(index=False))
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resumo das tarefas exportadas do Bubble")
    parser.add_argument("csv", nargs="?", default="tarefas_bubble_export.csv")
    parser.add_argument("--hoje", help="data de hoje (AAAA-MM-DD), para testes")
    args = parser.parse_args()
    analisar_tarefas(args.csv, args.hoje)
