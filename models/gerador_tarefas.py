import os
import shutil
import tempfile

import pandas as pd


class GeradorTarefas:
    COLUNAS = ["ID", "Título", "Categoria", "Prioridade", "Status"]

    def __init__(self, caminho=None):
        if caminho is None:
            raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho = os.path.join(raiz, "dados", "tarefas.csv")
        self.caminho = caminho

    def vazio(self):
        return pd.DataFrame(
            {
                "ID": pd.Series(dtype="int64"),
                "Título": pd.Series(dtype="object"),
                "Categoria": pd.Series(dtype="object"),
                "Prioridade": pd.Series(dtype="object"),
                "Status": pd.Series(dtype="object"),
            }
        )

    def carregar(self):
        if not os.path.isfile(self.caminho) or os.path.getsize(self.caminho) == 0:
            return self.vazio()
        try:
            df = pd.read_csv(
                self.caminho, encoding="utf-8-sig", dtype=str, keep_default_na=False
            )
            df = df[self.COLUNAS].copy()
            df["ID"] = pd.to_numeric(df["ID"]).astype("int64")
            if df["ID"].duplicated().any():
                raise ValueError("IDs repetidos")
        except Exception:
            self._guardar_copia_do_arquivo_invalido()
            return self.vazio()
        return df.reset_index(drop=True)

    def salvar(self, df):
        pasta = os.path.dirname(self.caminho)
        os.makedirs(pasta, exist_ok=True)
        descritor, temporario = tempfile.mkstemp(dir=pasta, suffix=".tmp")
        os.close(descritor)
        try:
            df[self.COLUNAS].to_csv(temporario, index=False, encoding="utf-8-sig")
            os.replace(temporario, self.caminho)
        except Exception:
            if os.path.exists(temporario):
                os.remove(temporario)
            raise

    def _guardar_copia_do_arquivo_invalido(self):
        try:
            shutil.copy2(self.caminho, self.caminho + ".invalido")
        except OSError:
            pass
