import importlib.util
import subprocess
import sys


def garantir_dependencias():
    faltando = [
        pacote
        for pacote in ("pandas", "matplotlib")
        if importlib.util.find_spec(pacote) is None
    ]
    if faltando:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *faltando])


def ativar_nitidez_no_windows():
    if sys.platform.startswith("win"):
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass


if __name__ == "__main__":
    garantir_dependencias()
    ativar_nitidez_no_windows()

    from models.gerador_tarefas import GeradorTarefas
    from controllers.controlador_tarefas import ControladorTarefas
    from views.tela_tarefas import TelaTarefas

    gerador = GeradorTarefas()
    controlador = ControladorTarefas(gerador)
    TelaTarefas(controlador).executar()
