import pandas as pd


class ControladorTarefas:
    CATEGORIAS = ("Trabalho", "Estudos", "Pessoal")
    PRIORIDADES = ("Baixa", "Média", "Alta")
    PENDENTE = "Pendente"
    CONCLUIDA = "Concluída"
    TAMANHO_MAXIMO_TITULO = 120

    def __init__(self, gerador):
        self.gerador = gerador
        self.df = gerador.carregar()

    def listar(self):
        return self.df.to_dict("records")

    def buscar(self, id_tarefa):
        linha = self.df[self.df["ID"] == id_tarefa]
        if linha.empty:
            raise ValueError("Tarefa não encontrada.")
        return linha.iloc[0].to_dict()

    def adicionar(self, titulo, categoria, prioridade):
        titulo = (titulo or "").strip()
        if not titulo:
            raise ValueError("Digite um título para a tarefa.")
        if len(titulo) > self.TAMANHO_MAXIMO_TITULO:
            raise ValueError(
                f"O título pode ter no máximo {self.TAMANHO_MAXIMO_TITULO} caracteres."
            )
        if categoria not in self.CATEGORIAS:
            raise ValueError("Escolha uma categoria.")
        if prioridade not in self.PRIORIDADES:
            raise ValueError("Escolha uma prioridade.")

        novo_id = int(self.df["ID"].max()) + 1 if not self.df.empty else 1
        nova = {
            "ID": novo_id,
            "Título": titulo,
            "Categoria": categoria,
            "Prioridade": prioridade,
            "Status": self.PENDENTE,
        }
        if self.df.empty:
            novo_df = pd.DataFrame([nova], columns=self.gerador.COLUNAS)
        else:
            novo_df = pd.concat([self.df, pd.DataFrame([nova])], ignore_index=True)
        novo_df["ID"] = novo_df["ID"].astype("int64")
        self.gerador.salvar(novo_df)
        self.df = novo_df
        return novo_id

    def marcar_concluida(self, id_tarefa):
        self.buscar(id_tarefa)
        novo_df = self.df.copy()
        indice = novo_df.index[novo_df["ID"] == id_tarefa][0]
        if novo_df.at[indice, "Status"] == self.CONCLUIDA:
            return False
        novo_df.at[indice, "Status"] = self.CONCLUIDA
        self.gerador.salvar(novo_df)
        self.df = novo_df
        return True

    def excluir(self, id_tarefa):
        self.buscar(id_tarefa)
        novo_df = self.df[self.df["ID"] != id_tarefa].reset_index(drop=True)
        self.gerador.salvar(novo_df)
        self.df = novo_df

    def indicadores(self):
        total = len(self.df)
        concluidas = int((self.df["Status"] == self.CONCLUIDA).sum())
        return {
            "total": total,
            "concluidas": concluidas,
            "pendentes": total - concluidas,
        }

    def contagem_por_categoria(self):
        contagem = self.df["Categoria"].value_counts()
        ordem = [c for c in self.CATEGORIAS if c in contagem.index]
        ordem += [c for c in contagem.index if c not in self.CATEGORIAS]
        return {categoria: int(contagem[categoria]) for categoria in ordem}

    def contagem_por_status(self):
        concluidas = int((self.df["Status"] == self.CONCLUIDA).sum())
        return {
            self.PENDENTE: len(self.df) - concluidas,
            self.CONCLUIDA: concluidas,
        }
