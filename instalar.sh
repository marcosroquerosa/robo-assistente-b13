#!/bin/bash
# ============================================================
#  INSTALAR O ROBO NA BTV B13 (rode uma vez, com internet)
#  Na pasta do projeto:   bash instalar.sh
# ============================================================
set -e
cd "$(dirname "$0")"
SUDO=""
[ "$(id -u)" -eq 0 ] || SUDO="sudo"

echo "[1/3] Instalando programas do sistema..."
$SUDO apt update
$SUDO apt install -y python3-venv python3-pip adb android-sdk-platform-tools-common unzip

# Permissão do USB para celulares Android de qualquer fabricante
# (o pacote android-sdk-platform-tools-common traz as regras do udev)
$SUDO udevadm control --reload-rules || true
$SUDO udevadm trigger || true

echo "[2/3] Criando o ambiente do robô (.venv) e instalando as bibliotecas..."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "[3/3] Baixando os modelos de ouvido, entendimento, voz e visão..."
.venv/bin/python ferramentas/baixar_modelos.py

chmod +x iniciar.sh ativar_modo_automatico.sh desativar_modo_automatico.sh
echo
echo "Tudo instalado! Antes de ligar o robô:"
echo "  1. Salve a chave do Gemini em chave_web.txt"
echo "  2. Coloque um e-mail de contato em IMAGENS_CONTATO, no robo/config.py"
echo
echo "  Para testar à mão:          ./iniciar.sh"
echo "  Para ligar sozinho sempre:  ./ativar_modo_automatico.sh"
