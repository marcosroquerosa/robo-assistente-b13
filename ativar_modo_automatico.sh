#!/bin/bash
# ============================================================
#  ATIVAR O MODO AUTOMÁTICO
#  Depois disto, o robô liga sozinho sempre que a B13 ligar,
#  sem precisar entrar no usuário. Rode:  ./ativar_modo_automatico.sh
# ============================================================
set -e
cd "$(dirname "$0")"
PASTA="$(pwd)"
USUARIO="$(whoami)"
SUDO=""
[ "$(id -u)" -eq 0 ] || SUDO="sudo"

echo "[1/4] Permissão para o robô usar o celular pelo cabo..."
# Regra para celulares Motorola (fabricante 22b8) e Samsung (04e8). Para outra marca,
# acrescente uma linha com o código que aparece em lsusb.
$SUDO tee /etc/udev/rules.d/51-robo-celular.rules >/dev/null <<EOF
SUBSYSTEM=="usb", ATTR{idVendor}=="22b8", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"
EOF
$SUDO usermod -aG plugdev "$USUARIO"
$SUDO udevadm control --reload-rules
$SUDO udevadm trigger

echo "[2/4] Impedindo a B13 de dormir..."
$SUDO systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

echo "[3/4] Criando o serviço do robô (robo-byte)..."
$SUDO tee /etc/systemd/system/robo-byte.service >/dev/null <<EOF
[Unit]
Description=Robo Byte - assistente de aulas
After=network-online.target
Wants=network-online.target

[Service]
User=$USUARIO
WorkingDirectory=$PASTA
Environment=PYTHONUNBUFFERED=1
ExecStart=$PASTA/.venv/bin/python $PASTA/ferramentas/automatico.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "[4/4] Ligando o serviço..."
$SUDO systemctl daemon-reload
$SUDO systemctl enable --now robo-byte

echo
echo "Modo automático ativo! O robô já está ligando."
echo "  Ver o que o robô está fazendo:  journalctl -u robo-byte -f"
echo "  Reiniciar o robô:               systemctl restart robo-byte"
echo "  Desligar o modo automático:     ./desativar_modo_automatico.sh"
