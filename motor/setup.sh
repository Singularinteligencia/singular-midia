#!/bin/bash
# Prepara o motor de artes da Singular numa máquina nova (caminhos fixos em /home/claude).
set -e
AQUI="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /home/claude/geo_dados /home/claude/fotos /mnt/user-data/outputs
cp "$AQUI"/*.py /home/claude/
cp "$AQUI"/geo_dados/br_states.json /home/claude/geo_dados/
[ -f "$AQUI/alerta_dp_noite.png" ] && cp "$AQUI/alerta_dp_noite.png" /home/claude/fotos/
F=/usr/share/fonts/truetype/google-fonts
if [ ! -f $F/Poppins-Bold.ttf ]; then (mkdir -p $F 2>/dev/null && cp "$AQUI"/fontes/*.ttf $F/) || (sudo mkdir -p $F && sudo cp "$AQUI"/fontes/*.ttf $F/); fi
python3 -c "import PIL, numpy, scipy, soundfile" 2>/dev/null || pip install --break-system-packages -q pillow numpy scipy soundfile
which ffmpeg >/dev/null || (sudo apt-get install -y -q ffmpeg || apt-get install -y -q ffmpeg)
echo "motor pronto"
