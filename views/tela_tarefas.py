import math
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COR = {
    "fundo": "#F5F6F8",
    "superficie": "#FFFFFF",
    "borda": "#D3D8E0",
    "grade": "#E6E9EF",
    "texto": "#1F2430",
    "texto_suave": "#566070",
    "texto_mudo": "#6B7280",
    "desabilitado": "#8B94A3",
    "acento": "#2B54D9",
    "acento_hover": "#2347B8",
    "acento_pressionado": "#1D3C9A",
    "selecao": "#DCE6FF",
    "cabecalho": "#EDF0F5",
    "hover": "#EEF1F6",
    "pressionado": "#E1E6EE",
    "perigo": "#B42318",
    "perigo_hover": "#FDECEA",
}

SERIE_CATEGORIAS = ["#2a78d6", "#eb6834", "#1baf7a"]
COR_CATEGORIA_EXTRA = "#7B8494"
COR_PENDENTE = "#7B8494"
COR_CONCLUIDA = "#0ca30c"


def escolher_fonte(root):
    familias = set(tkfont.families(root))
    for nome in ("Segoe UI", "Helvetica Neue", "Noto Sans", "DejaVu Sans", "Arial"):
        if nome in familias:
            return nome
    return tkfont.nametofont("TkDefaultFont").actual("family")


class TelaTarefas:
    def __init__(self, controlador):
        self.controlador = controlador
        self.janela_grafico = None

        self.root = tk.Tk()
        self.root.title("TaskMaster Pro")
        self.root.minsize(880, 580)
        self.root.configure(bg=COR["fundo"])

        self.fonte = escolher_fonte(self.root)
        self.f_pequena = (self.fonte, 9)
        self.f_negrito = (self.fonte, 10, "bold")
        self.f_secao = (self.fonte, 11, "bold")
        self.f_numero = (self.fonte, 13, "bold")

        self._configurar_estilo()
        self._montar()
        self._centralizar(1000, 680)
        self._atualizar()
        self.entry_titulo.focus_set()

    def _centralizar(self, largura, altura):
        self.root.update_idletasks()
        x = max((self.root.winfo_screenwidth() - largura) // 2, 0)
        y = max((self.root.winfo_screenheight() - altura) // 3, 0)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def _configurar_estilo(self):
        for nome in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont", "TkCaptionFont"):
            tkfont.nametofont(nome).configure(family=self.fonte, size=10)

        self.root.option_add("*TCombobox*Listbox.font", (self.fonte, 10))
        self.root.option_add("*TCombobox*Listbox.background", COR["superficie"])
        self.root.option_add("*TCombobox*Listbox.foreground", COR["texto"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", COR["selecao"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", COR["texto"])

        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")
        estilo.configure(".", font=(self.fonte, 10), background=COR["fundo"], foreground=COR["texto"])

        campo = dict(
            fieldbackground=COR["superficie"],
            background=COR["superficie"],
            foreground=COR["texto"],
            bordercolor=COR["borda"],
            lightcolor=COR["borda"],
            darkcolor=COR["borda"],
            padding=7,
            relief="flat",
        )
        foco = dict(
            bordercolor=[("focus", COR["acento"])],
            lightcolor=[("focus", COR["acento"])],
            darkcolor=[("focus", COR["acento"])],
        )
        estilo.configure("TEntry", insertcolor=COR["texto"], **campo)
        estilo.map("TEntry", **foco)
        estilo.configure("TCombobox", arrowcolor=COR["texto_suave"], arrowsize=14, **campo)
        estilo.map(
            "TCombobox",
            fieldbackground=[("readonly", COR["superficie"])],
            selectbackground=[("readonly", COR["superficie"])],
            selectforeground=[("readonly", COR["texto"])],
            **foco,
        )

        botao = dict(
            background=COR["superficie"],
            foreground=COR["texto"],
            bordercolor=COR["borda"],
            lightcolor=COR["superficie"],
            darkcolor=COR["superficie"],
            focuscolor=COR["acento"],
            padding=(14, 7),
            relief="flat",
        )
        estilo.configure("TButton", **botao)
        estilo.map(
            "TButton",
            background=[("disabled", COR["superficie"]), ("pressed", COR["pressionado"]), ("active", COR["hover"])],
            foreground=[("disabled", COR["desabilitado"])],
            bordercolor=[("disabled", COR["grade"])],
        )

        estilo.configure(
            "Primario.TButton",
            background=COR["acento"],
            foreground="#FFFFFF",
            bordercolor=COR["acento"],
            lightcolor=COR["acento"],
            darkcolor=COR["acento"],
            focuscolor="#FFFFFF",
            padding=(16, 7),
            relief="flat",
            font=self.f_negrito,
        )
        estilo.map(
            "Primario.TButton",
            background=[("pressed", COR["acento_pressionado"]), ("active", COR["acento_hover"])],
            bordercolor=[("pressed", COR["acento_pressionado"]), ("active", COR["acento_hover"])],
        )

        estilo.configure("Perigo.TButton", **botao)
        estilo.configure("Perigo.TButton", foreground=COR["perigo"])
        estilo.map(
            "Perigo.TButton",
            background=[("disabled", COR["superficie"]), ("pressed", COR["perigo_hover"]), ("active", COR["perigo_hover"])],
            foreground=[("disabled", COR["desabilitado"])],
            bordercolor=[("disabled", COR["grade"]), ("active", COR["perigo"])],
        )

        estilo.configure(
            "Treeview",
            background=COR["superficie"],
            fieldbackground=COR["superficie"],
            foreground=COR["texto"],
            rowheight=32,
            borderwidth=0,
            relief="flat",
        )
        estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        estilo.map(
            "Treeview",
            background=[("selected", COR["selecao"])],
            foreground=[("selected", COR["texto"])],
        )
        estilo.configure(
            "Treeview.Heading",
            background=COR["cabecalho"],
            foreground=COR["texto_suave"],
            font=self.f_negrito,
            relief="flat",
            borderwidth=0,
            padding=(10, 8),
        )
        estilo.map("Treeview.Heading", background=[("active", COR["cabecalho"])])

        estilo.configure(
            "Vertical.TScrollbar",
            background=COR["borda"],
            troughcolor=COR["superficie"],
            bordercolor=COR["superficie"],
            arrowcolor=COR["texto_suave"],
            relief="flat",
        )
        estilo.map("Vertical.TScrollbar", background=[("active", COR["desabilitado"])])

        estilo.configure("TNotebook", background=COR["superficie"], borderwidth=0, tabmargins=(16, 12, 16, 0))
        estilo.configure(
            "TNotebook.Tab",
            background=COR["superficie"],
            foreground=COR["texto_suave"],
            padding=(14, 8),
            borderwidth=0,
        )
        estilo.map(
            "TNotebook.Tab",
            foreground=[("selected", COR["acento"]), ("active", COR["texto"])],
            background=[("selected", COR["superficie"]), ("active", COR["hover"])],
        )

    def _cartao(self, pai):
        return tk.Frame(
            pai,
            bg=COR["superficie"],
            highlightbackground=COR["borda"],
            highlightcolor=COR["borda"],
            highlightthickness=1,
        )

    def _rotulo(self, pai, texto, fonte=None, cor="texto", fundo="superficie"):
        return tk.Label(
            pai,
            text=texto,
            font=fonte or (self.fonte, 10),
            bg=COR[fundo],
            fg=COR[cor],
            anchor="w",
        )

    def _montar(self):
        raiz = self.root
        margem = 20
        raiz.columnconfigure(0, weight=1)
        raiz.rowconfigure(2, weight=1)

        cartao_form = self._cartao(raiz)
        cartao_form.grid(row=0, column=0, sticky="ew", padx=margem, pady=(margem, 12))
        cartao_form.columnconfigure(0, weight=1)

        self._rotulo(cartao_form, "Nova tarefa", self.f_secao).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(14, 10)
        )
        self._rotulo(cartao_form, "Título", self.f_pequena, "texto_suave").grid(
            row=1, column=0, sticky="w", padx=(16, 8)
        )
        self._rotulo(cartao_form, "Categoria", self.f_pequena, "texto_suave").grid(
            row=1, column=1, sticky="w", padx=8
        )
        self._rotulo(cartao_form, "Prioridade", self.f_pequena, "texto_suave").grid(
            row=1, column=2, sticky="w", padx=8
        )

        limite = self.controlador.TAMANHO_MAXIMO_TITULO
        validar = (self.root.register(lambda proposto: len(proposto) <= limite), "%P")
        self.var_titulo = tk.StringVar()
        self.entry_titulo = ttk.Entry(
            cartao_form, textvariable=self.var_titulo, validate="key", validatecommand=validar
        )
        self.entry_titulo.grid(row=2, column=0, sticky="ew", padx=(16, 8), pady=(2, 0))

        self.combo_categoria = ttk.Combobox(
            cartao_form, values=self.controlador.CATEGORIAS, state="readonly", width=14
        )
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=2, column=1, padx=8, pady=(2, 0))

        self.combo_prioridade = ttk.Combobox(
            cartao_form, values=self.controlador.PRIORIDADES, state="readonly", width=12
        )
        self.combo_prioridade.set("Média")
        self.combo_prioridade.grid(row=2, column=2, padx=8, pady=(2, 0))

        self.btn_adicionar = ttk.Button(
            cartao_form, text="Adicionar Tarefa", style="Primario.TButton", command=self.adicionar_acao
        )
        self.btn_adicionar.grid(row=2, column=3, padx=(8, 16), pady=(2, 0))

        self.lbl_erro = tk.Label(
            cartao_form, text="", font=(self.fonte, 9), bg=COR["superficie"], fg=COR["perigo"], anchor="w", height=1
        )
        self.lbl_erro.grid(row=3, column=0, columnspan=4, sticky="ew", padx=16, pady=(6, 10))

        cartao_kpi = self._cartao(raiz)
        cartao_kpi.grid(row=1, column=0, sticky="ew", padx=margem, pady=(0, 12))
        cartao_kpi.columnconfigure(3, weight=1)

        self.val_total = self._kpi(cartao_kpi, 0, "Total de tarefas")
        self.val_concluidas = self._kpi(cartao_kpi, 1, "Concluídas")
        self.val_pendentes = self._kpi(cartao_kpi, 2, "Pendentes")

        self.btn_grafico = ttk.Button(
            cartao_kpi, text="Gerar Gráfico de Produtividade", command=self.gerar_grafico_acao
        )
        self.btn_grafico.grid(row=0, column=4, padx=14, pady=10, sticky="e")

        cartao_tabela = self._cartao(raiz)
        cartao_tabela.grid(row=2, column=0, sticky="nsew", padx=margem)
        cartao_tabela.columnconfigure(0, weight=1)
        cartao_tabela.rowconfigure(0, weight=1)

        colunas = ("ID", "Título", "Categoria", "Prioridade", "Status")
        self.tree = ttk.Treeview(cartao_tabela, columns=colunas, show="headings", selectmode="browse")
        larguras = {"ID": 64, "Título": 380, "Categoria": 130, "Prioridade": 120, "Status": 130}
        for coluna in colunas:
            alinhamento = "w" if coluna != "ID" else "center"
            self.tree.heading(coluna, text=coluna, anchor=alinhamento)
            self.tree.column(
                coluna,
                width=larguras[coluna],
                minwidth=larguras[coluna] if coluna != "Título" else 160,
                anchor=alinhamento,
                stretch=(coluna == "Título"),
            )
        self.tree.tag_configure("concluida", foreground=COR["texto_mudo"])
        self.tree.tag_configure("alta", foreground=COR["perigo"])

        rolagem = ttk.Scrollbar(cartao_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=rolagem.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        rolagem.grid(row=0, column=1, sticky="ns")

        self.lbl_vazio = tk.Label(
            cartao_tabela,
            text="Nenhuma tarefa cadastrada.\nDigite um título acima e clique em Adicionar Tarefa.",
            font=(self.fonte, 10),
            bg=COR["superficie"],
            fg=COR["texto_suave"],
            justify="center",
        )

        barra_acoes = tk.Frame(raiz, bg=COR["fundo"])
        barra_acoes.grid(row=3, column=0, sticky="ew", padx=margem, pady=(12, margem))

        self.btn_concluir = ttk.Button(
            barra_acoes, text="Marcar como Concluída", command=self.concluir_acao
        )
        self.btn_concluir.pack(side=tk.LEFT)
        self.btn_excluir = ttk.Button(
            barra_acoes, text="Excluir Tarefa", style="Perigo.TButton", command=self.excluir_acao
        )
        self.btn_excluir.pack(side=tk.LEFT, padx=(8, 0))

        self.lbl_dica = tk.Label(
            barra_acoes, text="", font=(self.fonte, 9), bg=COR["fundo"], fg=COR["texto_suave"]
        )
        self.lbl_dica.pack(side=tk.LEFT, padx=16)

        self.entry_titulo.bind("<Return>", lambda evento: self.adicionar_acao())
        self.entry_titulo.bind("<Key>", lambda evento: self._limpar_erro(), add="+")
        self.tree.bind("<<TreeviewSelect>>", lambda evento: self._ao_selecionar())
        self.tree.bind("<Delete>", lambda evento: self.excluir_acao())

    def _kpi(self, pai, coluna, rotulo):
        grupo = tk.Frame(pai, bg=COR["superficie"])
        grupo.grid(row=0, column=coluna, padx=(18 if coluna == 0 else 0, 0), pady=10, sticky="w")
        if coluna > 0:
            tk.Frame(grupo, bg=COR["borda"], width=1, height=22).pack(side=tk.LEFT, padx=(0, 18))
        tk.Label(
            grupo, text=rotulo, font=(self.fonte, 10), bg=COR["superficie"], fg=COR["texto_suave"]
        ).pack(side=tk.LEFT)
        valor = tk.Label(
            grupo, text="0", font=self.f_numero, bg=COR["superficie"], fg=COR["texto"]
        )
        valor.pack(side=tk.LEFT, padx=(8, 18))
        return valor

    def _limpar_erro(self):
        self.lbl_erro.config(text="")

    def _mostrar_erro(self, mensagem):
        self.lbl_erro.config(text=mensagem)

    def _atualizar(self, selecionar=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tarefas = self.controlador.listar()
        for tarefa in tarefas:
            if tarefa["Status"] == self.controlador.CONCLUIDA:
                tags = ("concluida",)
            elif tarefa["Prioridade"] == "Alta":
                tags = ("alta",)
            else:
                tags = ()
            self.tree.insert(
                "",
                tk.END,
                iid=str(tarefa["ID"]),
                values=(
                    tarefa["ID"],
                    tarefa["Título"],
                    tarefa["Categoria"],
                    tarefa["Prioridade"],
                    tarefa["Status"],
                ),
                tags=tags,
            )

        if tarefas:
            self.lbl_vazio.place_forget()
        else:
            self.lbl_vazio.place(relx=0.5, rely=0.42, anchor="center")

        indicadores = self.controlador.indicadores()
        self.val_total.config(text=str(indicadores["total"]))
        self.val_concluidas.config(text=str(indicadores["concluidas"]))
        self.val_pendentes.config(text=str(indicadores["pendentes"]))

        if selecionar is not None and self.tree.exists(str(selecionar)):
            self.tree.selection_set(str(selecionar))
            self.tree.see(str(selecionar))
        self._ao_selecionar()

    def _id_selecionado(self):
        selecao = self.tree.selection()
        return int(selecao[0]) if selecao else None

    def _ao_selecionar(self):
        id_tarefa = self._id_selecionado()
        if id_tarefa is None:
            self.btn_concluir.state(["disabled"])
            self.btn_excluir.state(["disabled"])
            self.lbl_dica.config(text="Selecione uma tarefa na tabela para marcar como concluída ou excluir.")
        else:
            tarefa = self.controlador.buscar(id_tarefa)
            ja_concluida = tarefa["Status"] == self.controlador.CONCLUIDA
            self.btn_concluir.state(["disabled"] if ja_concluida else ["!disabled"])
            self.btn_excluir.state(["!disabled"])
            self.lbl_dica.config(text="")
        if self.controlador.indicadores()["total"] == 0:
            self.btn_grafico.state(["disabled"])
        else:
            self.btn_grafico.state(["!disabled"])

    def _erro_ao_salvar(self):
        self._mostrar_erro(
            "Não foi possível salvar em dados/tarefas.csv. Feche o arquivo se ele estiver aberto em outro programa."
        )

    def adicionar_acao(self):
        try:
            novo_id = self.controlador.adicionar(
                self.var_titulo.get(),
                self.combo_categoria.get(),
                self.combo_prioridade.get(),
            )
        except ValueError as erro:
            self._mostrar_erro(str(erro))
            self.entry_titulo.focus_set()
            return
        except OSError:
            self._erro_ao_salvar()
            return
        self._limpar_erro()
        self.var_titulo.set("")
        self._atualizar(selecionar=novo_id)
        self.entry_titulo.focus_set()

    def concluir_acao(self):
        id_tarefa = self._id_selecionado()
        if id_tarefa is None:
            return
        try:
            self.controlador.marcar_concluida(id_tarefa)
        except ValueError as erro:
            self._mostrar_erro(str(erro))
        except OSError:
            self._erro_ao_salvar()
            return
        self._limpar_erro()
        self._atualizar(selecionar=id_tarefa)

    def excluir_acao(self):
        id_tarefa = self._id_selecionado()
        if id_tarefa is None:
            return
        titulo = self.controlador.buscar(id_tarefa)["Título"]
        confirmou = messagebox.askyesno(
            "Excluir tarefa",
            f"Excluir a tarefa \"{titulo}\"?\nEssa ação não pode ser desfeita.",
            parent=self.root,
        )
        if not confirmou:
            return
        try:
            self.controlador.excluir(id_tarefa)
        except ValueError as erro:
            self._mostrar_erro(str(erro))
        except OSError:
            self._erro_ao_salvar()
            return
        self._limpar_erro()
        self._atualizar()

    def gerar_grafico_acao(self):
        if self.controlador.indicadores()["total"] == 0:
            messagebox.showinfo(
                "Gráfico de produtividade",
                "Cadastre pelo menos uma tarefa para gerar o gráfico.",
                parent=self.root,
            )
            return None

        if self.janela_grafico is not None and self.janela_grafico.winfo_exists():
            self.janela_grafico.destroy()

        janela = tk.Toplevel(self.root)
        janela.title("Gráfico de Produtividade")
        janela.configure(bg=COR["superficie"])
        janela.geometry("760x540")
        janela.minsize(560, 420)
        janela.transient(self.root)

        abas = ttk.Notebook(janela)
        abas.pack(fill=tk.BOTH, expand=True)

        for titulo_aba, criar_figura in (
            ("Por categoria", self._figura_categorias),
            ("Por status", self._figura_status),
        ):
            quadro = tk.Frame(abas, bg=COR["superficie"])
            abas.add(quadro, text=titulo_aba)
            figura = criar_figura()
            canvas = FigureCanvasTkAgg(figura, master=quadro)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        self.janela_grafico = janela
        return janela

    def _nova_figura(self):
        figura = Figure(figsize=(7, 4.6), dpi=100, facecolor=COR["superficie"])
        figura.subplots_adjust(left=0.1, right=0.95, top=0.88, bottom=0.14)
        return figura

    def _figura_categorias(self):
        dados = {c: n for c, n in self.controlador.contagem_por_categoria().items() if n > 0}
        figura = self._nova_figura()
        ax = figura.add_subplot(111)
        total = sum(dados.values())
        categorias = list(dados.keys())
        valores = list(dados.values())
        conhecidas = list(self.controlador.CATEGORIAS)
        cores = [
            SERIE_CATEGORIAS[conhecidas.index(c)] if c in conhecidas else COR_CATEGORIA_EXTRA
            for c in categorias
        ]
        fatias, _ = ax.pie(
            valores,
            colors=cores,
            startangle=90,
            counterclock=False,
            radius=0.85,
            wedgeprops={"edgecolor": COR["superficie"], "linewidth": 2},
        )
        for fatia, categoria, valor in zip(fatias, categorias, valores):
            angulo = math.radians((fatia.theta1 + fatia.theta2) / 2)
            x, y = math.cos(angulo), math.sin(angulo)
            ax.annotate(
                f"{categoria}\n{valor} ({valor / total:.0%})",
                xy=(0.85 * x, 0.85 * y),
                xytext=(1.12 * x, 1.12 * y),
                ha="left" if x >= 0 else "right",
                va="center",
                fontsize=10,
                color=COR["texto"],
            )
        ax.legend(
            fatias,
            categorias,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=max(len(categorias), 1),
            frameon=False,
            labelcolor=COR["texto"],
            fontsize=10,
        )
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        figura.suptitle(
            "Tarefas por categoria", x=0.05, ha="left", fontsize=13, fontweight="bold", color=COR["texto"]
        )
        return figura

    def _figura_status(self):
        dados = self.controlador.contagem_por_status()
        figura = self._nova_figura()
        ax = figura.add_subplot(111)
        nomes = list(dados.keys())
        valores = list(dados.values())
        cores = [COR_PENDENTE if n == self.controlador.PENDENTE else COR_CONCLUIDA for n in nomes]
        barras = ax.bar(nomes, valores, width=0.42, color=cores)
        topo = max(max(valores), 1)
        for barra, valor in zip(barras, valores):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                valor + topo * 0.02,
                str(valor),
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
                color=COR["texto"],
            )
        ax.set_ylim(0, topo * 1.18)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylabel("Tarefas", color=COR["texto_suave"], fontsize=10)
        ax.set_axisbelow(True)
        ax.grid(axis="y", color=COR["grade"], linewidth=1)
        for lado in ("top", "right", "left"):
            ax.spines[lado].set_visible(False)
        ax.spines["bottom"].set_color(COR["borda"])
        ax.tick_params(axis="both", colors=COR["texto_suave"], labelsize=10, length=0)
        ax.tick_params(axis="x", labelcolor=COR["texto"], labelsize=11, pad=8)
        ax.set_facecolor(COR["superficie"])
        figura.suptitle(
            "Tarefas por status", x=0.05, ha="left", fontsize=13, fontweight="bold", color=COR["texto"]
        )
        return figura

    def executar(self):
        self.root.mainloop()
