# TaskMaster Pro — Gerenciador de Tarefas Desktop

Aplicativo desktop para organizar tarefas do dia a dia, feito em **Python** com **Tkinter**. Você cadastra tarefas por categoria e prioridade, acompanha o que está pendente ou concluído e visualiza sua produtividade em gráficos. Tudo é salvo automaticamente em um arquivo CSV, então não precisa de banco de dados nem de internet.

## Funcionalidades

- **Cadastro de tarefas** com título (até 120 caracteres), categoria (*Trabalho*, *Estudos* ou *Pessoal*) e prioridade (*Baixa*, *Média* ou *Alta*)
- **Tabela de tarefas** com ID, título, categoria, prioridade e status; tarefas de prioridade alta ficam destacadas em vermelho e as concluídas ficam em cinza
- **Marcar como concluída** e **excluir** tarefas (com confirmação antes de apagar; a tecla `Delete` também funciona)
- **Indicadores** no topo: total de tarefas, concluídas e pendentes
- **Gráfico de produtividade** em uma janela com duas abas:
  - *Por categoria*: gráfico de pizza com a quantidade e a porcentagem de cada categoria
  - *Por status*: gráfico de barras com pendentes × concluídas
- **Salvamento automático** em `dados/tarefas.csv`, com gravação segura (arquivo temporário substituído no final) para evitar perda de dados
- **Proteção contra arquivo corrompido**: se o CSV estiver inválido, o app guarda uma cópia como `tarefas.csv.invalido` e começa com a lista vazia
- Interface com janela centralizada, fonte escolhida conforme o sistema e nitidez ajustada no Windows (DPI)

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3 | Linguagem principal (desenvolvido com Python 3.12) |
| Tkinter / ttk | Interface gráfica |
| pandas | Leitura, escrita e manipulação dos dados |
| Matplotlib | Gráficos de produtividade |

## Estrutura do projeto

O projeto segue o padrão **MVC**:

```
TaskMasterPro-Gerenciador-de-Tarefas-Desktop/
├── main.py                       # Ponto de entrada do aplicativo
├── requirements.txt              # Dependências (pandas e matplotlib)
├── models/
│   └── gerador_tarefas.py        # Model: carrega e salva o CSV
├── controllers/
│   └── controlador_tarefas.py    # Controller: regras de negócio e validações
├── views/
│   └── tela_tarefas.py           # View: interface Tkinter e gráficos
└── dados/
    └── tarefas.csv               # Arquivo onde as tarefas ficam salvas
```

## Como executar

### Pré-requisitos

- [Python 3.8 ou superior](https://www.python.org/downloads/) com Tkinter (já vem junto no instalador oficial para Windows e macOS)
- No Linux, talvez seja preciso instalar o Tkinter separadamente, por exemplo: `sudo apt install python3-tk`

### Passo a passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/miguel-neri17/TaskMasterPro-Gerenciador-de-Tarefas-Desktop.git
   cd TaskMasterPro-Gerenciador-de-Tarefas-Desktop
   ```

2. (Opcional) Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   > Se você pular este passo, o `main.py` instala `pandas` e `matplotlib` sozinho na primeira execução, caso não estejam instalados.

4. Execute o aplicativo:

   ```bash
   python main.py
   ```

## Como usar

1. Digite o título da tarefa, escolha a categoria e a prioridade e clique em **Adicionar Tarefa** (ou aperte `Enter`).
2. Selecione uma tarefa na tabela para **Marcar como Concluída** ou **Excluir Tarefa**.
3. Acompanhe os números de total, concluídas e pendentes no painel superior.
4. Clique em **Gerar Gráfico de Produtividade** para ver a distribuição por categoria e por status.

## Formato dos dados

As tarefas ficam em `dados/tarefas.csv` (codificação UTF-8) com as colunas:

| Coluna | Descrição |
|---|---|
| `ID` | Número único da tarefa, gerado automaticamente |
| `Título` | Descrição da tarefa |
| `Categoria` | Trabalho, Estudos ou Pessoal |
| `Prioridade` | Baixa, Média ou Alta |
| `Status` | Pendente ou Concluída |

> Se o aplicativo avisar que não conseguiu salvar, feche o `tarefas.csv` caso ele esteja aberto no Excel ou em outro programa.

## Ideias para o futuro

- Edição do título, da categoria e da prioridade de uma tarefa existente
- Filtros e busca na tabela
- Datas de vencimento e lembretes
- Gerar um executável (`.exe`) para distribuir o app

## Autor

**Miguel Neri** — estudante de Ciência de Dados

- GitHub: [@miguel-neri17](https://github.com/miguel-neri17)
- LinkedIn: [miguel-neri](https://www.linkedin.com/in/miguel-neri-a427b3420)
