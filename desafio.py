import pandas as pd
import numpy as np

df = pd.read_csv("Cópia de Base_Membros_Desempenho - Base_Membros_Desempenho.csv")



id_original = df["id_membro"].copy()


df["Nivel_Senioridade"] = df["Nivel_Senioridade"].replace(["N/D", "n/d", "N/d", "n/D"], pd.NA)
df["Nivel_Senioridade"] = df["Nivel_Senioridade"].apply(
    lambda x: "Pleno" if isinstance(x, str) and x.lower().startswith("p")
    else "Júnior" if isinstance(x, str) and x.lower().startswith("j")
    else "Sênior" if isinstance(x, str) and x.lower().startswith("s")
    else x
)
moda = df["Nivel_Senioridade"].mode()[0]
df["Nivel_Senioridade"].fillna(moda, inplace=True)


df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].replace(["N/D", "n/d", "N/d", "n/D"], np.nan)
df["Avaliacao_Tecnica"] = pd.to_numeric(df["Avaliacao_Tecnica"], errors="coerce")
media_tecnica = df["Avaliacao_Tecnica"].mean()
df["Avaliacao_Tecnica"].fillna(media_tecnica, inplace=True)


df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].replace(["N/D", "n/d", "N/d", "n/D"], np.nan)
df["Avaliacao_Comportamental"] = pd.to_numeric(df["Avaliacao_Comportamental"], errors="coerce")
media_comp = df["Avaliacao_Comportamental"].mean()
df["Avaliacao_Comportamental"].fillna(media_comp, inplace=True)


df["Engajamento_PIGs"] = df["Engajamento_PIGs"].astype(str).str.replace("%", "", regex=False)
df["Engajamento_PIGs"] = pd.to_numeric(df["Engajamento_PIGs"], errors="coerce") / 100
media_pigs = df["Engajamento_PIGs"].mean()
df["Engajamento_PIGs"].fillna(media_pigs, inplace=True)


df["Score_Desempenho"] = (df["Avaliacao_Tecnica"] * 0.5) + (df["Avaliacao_Comportamental"] * 0.5)


df["Status_Membro"] = df.apply(
    lambda row: "Destaque" if (row["Score_Desempenho"] >= 7) and (row["Engajamento_PIGs"] >= 0.8)
    else "Padrão",
    axis=1
)


colunas_numericas = df.select_dtypes(include=[np.number]).columns

for col in colunas_numericas:
    df[col] = df[col].apply(lambda x: f"{x:.2f}".replace(".", ","))


df["id_membro"] = id_original

df.to_csv("Base_Membros_Desempenho_Tratada.csv", index=False, encoding="utf-8-sig")
