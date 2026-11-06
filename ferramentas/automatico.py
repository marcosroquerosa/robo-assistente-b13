"""
MODO AUTOMÁTICO
===============
Liga o robô sozinho e cuida do celular. Roda como o serviço robo-byte, junto com a B13
(criado por ativar_modo_automatico.sh).

O que ele faz, em ordem:
  1. Liga o servidor do robô e espera ele carregar.
  2. Fica de olho no celular. Quando o celular aparece no cabo:
       - abre o caminho do celular até o computador (adb reverse)
       - mantém a tela ligada enquanto estiver no cabo
       - deixa a tela na horizontal
       - acorda a tela e abre o rosto no Chrome
       - "toca" na tela para ligar o som e o microfone
  3. Se o servidor cair, liga de novo. Se o celular sair do cabo e voltar, prepara de novo.

Para testar à mão:   .venv/bin/python ferramentas/automatico.py
"""

import os
import re
import subprocess
import sys
import time
import urllib.request

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PASTA)
sys.path.insert(0, PASTA)
from robo import config  # noqa: E402

ADB = "adb"
ENDERECO = f"http://localhost:{config.PORTA}"


def anotar(texto):
    print(time.strftime("%H:%M:%S"), "[automático]", texto, flush=True)


def adb(*argumentos, tempo_maximo=20) -> str:
    """Roda um comando do adb e devolve o que ele respondeu."""
    try:
        resultado = subprocess.run([ADB, *argumentos], capture_output=True, text=True, timeout=tempo_maximo)
        return resultado.stdout.strip()
    except Exception as erro:
        anotar(f"adb falhou ({' '.join(argumentos)}): {erro}")
        return ""


def responde(endereco) -> bool:
    try:
        urllib.request.urlopen(endereco, timeout=2)
        return True
    except Exception:
        return False


def esperar(condicao, segundos, nome) -> bool:
    for _ in range(segundos):
        if condicao():
            return True
        time.sleep(1)
    anotar(f"cansei de esperar: {nome}")
    return False


def celular_conectado() -> bool:
    return adb("get-state", tempo_maximo=5) == "device"


def ligar_servidor():
    anotar("ligando o servidor do robô...")
    return subprocess.Popen([sys.executable, "-m", "robo.servidor"])


def preparar_celular():
    anotar("celular conectado: preparando...")
    adb("reverse", f"tcp:{config.PORTA}", f"tcp:{config.PORTA}")
    adb("shell", "svc", "power", "stayon", "usb")                       # tela sempre ligada no cabo
    adb("shell", "settings", "put", "system", "accelerometer_rotation", "0")
    adb("shell", "settings", "put", "system", "user_rotation", "1")     # horizontal
    adb("shell", "input", "keyevent", "KEYCODE_WAKEUP")                 # acorda a tela
    adb("shell", "wm", "dismiss-keyguard")                              # tira a tela de bloqueio (sem senha)
    # o "application_id" faz o Chrome reaproveitar a mesma aba, em vez de abrir uma nova a cada vez
    adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", ENDERECO,
        "--es", "com.android.browser.application_id", "robo-byte", "com.android.chrome")
    time.sleep(6)                                                        # espera a página abrir
    # O Chrome só libera som e microfone depois de um toque: tocamos no meio da tela.
    tamanho = re.search(r"(\d+)x(\d+)", adb("shell", "wm", "size"))
    lado = min(int(tamanho.group(1)), int(tamanho.group(2))) if tamanho else 700
    adb("shell", "input", "tap", str(lado // 2), str(lado // 2))
    anotar("rosto aberto no celular.")


def main():
    anotar("modo automático começando")
    adb("start-server")

    servidor = ligar_servidor()
    esperar(lambda: responde(ENDERECO), 300, "servidor do robô")   # carregar os modelos demora

    celular_antes = False
    while True:
        if servidor.poll() is not None:
            anotar("o servidor parou; ligando de novo...")
            servidor = ligar_servidor()
            esperar(lambda: responde(ENDERECO), 300, "servidor do robô")
            # não reabre o rosto: a página no celular se reconecta sozinha ao servidor

        celular_agora = celular_conectado()
        if celular_agora and not celular_antes:
            preparar_celular()
        elif celular_agora:
            adb("reverse", f"tcp:{config.PORTA}", f"tcp:{config.PORTA}")  # garante o caminho (é rápido)
        elif celular_antes:
            anotar("celular desconectado; esperando ele voltar...")
        celular_antes = celular_agora
        time.sleep(5)


if __name__ == "__main__":
    main()
