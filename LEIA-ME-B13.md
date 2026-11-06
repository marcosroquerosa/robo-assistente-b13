# Robô Byte na BTV B13: passo a passo

## 1. Instalar o Debian na B13

Siga o [tutorial do projeto gabclima/b13](https://github.com/gabclima/b13/blob/main/TUTORIAL.md). O método usa um pendrive de 8 GB ou mais e não precisa de solda.

- **A instalação apaga o Android.** Faça antes o backup completo pedido no tutorial.
- No `boot.config`, use `box=s905x4_generic`. Não use a opção `gigabit`.
- Não rode `aml-multiboot-setup.sh`. O instalador do tutorial substitui esse passo.

Depois da instalação, a B13 liga sozinha na tomada. Para a configuração, use uma TV ou monitor pelo HDMI e um teclado USB.

## 2. Entrar na B13 pela rede (opcional)

Como `root`:

```bash
passwd
apt install -y openssh-server
systemctl enable --now ssh
adduser seunome
usermod -aG sudo seunome
hostname -I
```

No computador, use `ssh seunome@IP_DA_B13`. Para virar administrador, rode `sudo -i`. Não abra a porta 22 no roteador. Para acessar de fora da sua rede, use uma rede privada, como o Tailscale.

## 3. Instalar o robô (uma vez, com internet)

Com o cabo de rede ligado, como `root`:

```bash
apt install -y git
cd /root
git clone https://github.com/marcosroquerosa/robo-assistente-b13
cd robo-assistente-b13
bash instalar.sh
```

Ele instala os programas e as bibliotecas e baixa os modelos. Pode demorar bastante na primeira vez.

## 4. Colocar a chave do Gemini

1. Crie uma chave em aistudio.google.com.
2. Salve a chave na pasta do projeto:
   ```bash
   nano chave_web.txt
   chmod 600 chave_web.txt
   ```
   Cole a chave, salve com Ctrl+O e Enter e saia com Ctrl+X.

Esta versão precisa da chave para conversar. Se a internet cair, o robô avisa que está sem internet. No modo web, o texto das perguntas vai para o serviço escolhido, mas o áudio não. Confira os termos de uso antes de usar com alunos.

## 5. Testar à mão

1. Ligue o celular na B13 pelo cabo e aceite "Permitir depuração USB", marcando "Sempre permitir deste computador".
2. Confira: `adb devices` deve mostrar um código seguido de `device`.
3. Ligue o robô:
   ```bash
   ./iniciar.sh
   ```
4. Espere aparecer `Byte está no ar!`.
5. No Chrome do celular, abra `http://localhost:8000`, toque na tela e permita o microfone e a câmera.

Para desligar: Ctrl+C no terminal.

## 6. Modo automático (liga sozinho com a B13)

```bash
./ativar_modo_automatico.sh
```

Depois disso, o robô vira um serviço do sistema: liga junto com a B13, mesmo sem ninguém entrar no usuário, e religa sozinho se cair.

No celular, deixe o bloqueio de tela em "Nenhum" e permita o microfone e a câmera uma vez à mão.

| Para | Comando |
| --- | --- |
| Ver o que o robô está fazendo (e os tempos) | `journalctl -u robo-byte -f` |
| Reiniciar o robô (depois de mudar o config.py) | `systemctl restart robo-byte` |
| Parar até o próximo boot | `systemctl stop robo-byte` |
| Desligar o modo automático | `./desativar_modo_automatico.sh` |

Teste o ciclo completo: tire a B13 da tomada, ligue de novo e veja se o rosto volta sozinho. Depois, tire e recoloque o cabo do celular.

## 7. Visão: câmera, fotos e reconhecer pessoas

O robô usa a câmera da frente do celular. O instalador já baixa os modelos de rostos e mãos. Para baixar de novo:

```bash
.venv/bin/python ferramentas/baixar_modelos.py visao
systemctl restart robo-byte
```

**O que ele faz sozinho:** abre os olhos quando alguém chega, olha para quem está falando, atende quem levanta a mão e cumprimenta pelo nome quem já foi cadastrado (no máximo uma vez a cada 30 minutos).

**O que dá para pedir:**

| Diga | O robô |
| --- | --- |
| "aprende meu rosto" (ou "meu nome é Ana, aprende meu rosto") | pergunta o nome, pede para você olhar a tela e cadastra |
| "quem sou eu?", "quem você está vendo?" | responde sem internet |
| "esquece o rosto da Ana", "esquece meu rosto" | apaga o cadastro da pessoa |
| "tira uma foto" | conta 3, 2, 1, mostra a foto e guarda na pasta `fotos/` |
| "o que você está vendo?", "lê o quadro", "o que é isso na minha mão?" | manda a foto para o Gemini e responde |

**Privacidade (LGPD):**

- O reconhecimento roda todo na B13. O arquivo `dados/rostos.json` guarda só uma "assinatura" numérica de cada rosto, nunca a foto.
- Para a internet só vai a foto de quando alguém pede para o robô olhar. Nessa hora aparece na tela o aviso laranja "foto enviada para a IA na internet". Essas fotos não são guardadas.
- Rosto é dado biométrico sensível. Para cadastrar alunos, peça autorização dos responsáveis e da escola.
- Cada recurso liga e desliga no `robo/config.py`, na parte "Visão".

**Gerenciar o cadastro pelo teclado:**

```bash
.venv/bin/python ferramentas/rostos.py listar
.venv/bin/python ferramentas/rostos.py renomear Ana "Ana Clara"
.venv/bin/python ferramentas/rostos.py apagar Ana
.venv/bin/python ferramentas/rostos.py apagar-todos
```

Depois de mexer no cadastro pelo teclado, reinicie o robô.

**Ajustes comuns:**

- Os olhos olham para o lado errado: no `rosto/rosto.js`, troque `INVERTER_OLHAR = false` para `true`.
- Confunde pessoas: aumente `VISAO_LIMIAR_DE_PARECIDO` (ex.: 0.45). Não reconhece: diminua (ex.: 0.36) ou cadastre a pessoa de novo. As assinaturas novas se somam às antigas.
- A mão não é detectada: diminua `VISAO_CERTEZA_DA_MAO` (ex.: 0.4). Isso aumenta os alarmes falsos.
- Testar o reconhecimento com uma foto: `.venv/bin/python ferramentas/rostos.py testar foto.jpg`.

**Se o robô ficar lento**, faça uma mudança de cada vez, nesta ordem:

1. `VISAO_LARGURA_DO_QUADRO = 320`. Pessoas mais longe podem deixar de ser reconhecidas.
2. `VISAO_OLHAR_QUEM_FALA = False`.
3. `VISAO_MAO_LEVANTADA = False`.

Não baixe `VISAO_QUADROS_POR_SEGUNDO` para menos de 2 com a mão levantada ou o olhar para quem fala ligados.

## 8. Mostrar imagens ("Byte, mostra uma placa-mãe")

O robô procura o assunto na **Wikipédia em português** e no **Wikimedia Commons** e mostra a imagem na tela do celular, explicando em voz alta. Não precisa de chave nem de cadastro, só de internet.

1. A Wikipédia e o Commons exigem um contato de quem usa a busca, senão bloqueiam (erro 403). No `robo/config.py`, coloque seu e-mail em `IMAGENS_CONTATO`, por exemplo `IMAGENS_CONTATO = "professor@escola.com"`. Não envie esse e-mail para um repositório público.
2. Reinicie: `systemctl restart robo-byte`.

Para testar sem o robô: `.venv/bin/python -m robo.imagens placa-mãe` (só lista o que achou).

| Diga | O robô |
| --- | --- |
| "mostra uma placa-mãe", "quero ver uma memória RAM" | busca, mostra e explica |
| "mostra outra", "a próxima" | a próxima imagem da mesma busca, alternando as duas fontes |
| "fecha a imagem" (ou toque na tela) | tira a imagem da tela |

**Como ele cuida da turma:**

- As imagens têm licença livre. Embaixo da imagem aparece o artigo de onde ela veio ou, no Commons, o autor e a licença.
- Antes de mostrar, o Gemini confere se a imagem é mesmo o que foi pedido e se serve para a turma. Se não servir, ele tenta a próxima.
- O Commons guarda fotos de todo tipo, então só entra na busca quando o Gemini pode conferir as imagens.
- Para escolher as fontes, mude `IMAGENS_FONTES` no `config.py`. No Commons, muitas descrições estão em inglês, então a busca em português acha menos imagens por lá.
- Nenhuma imagem é gravada no disco: ela fica só na memória e é apagada quando sai da tela (depois de 60 segundos, com um toque ou com "fecha a imagem").
- Às vezes a imagem principal do artigo é um desenho ou um esquema, e não uma foto. Se não servir, peça "mostra outra" ou use um nome mais específico ("mostra um pente de memória RAM").

## 9. Wi-Fi

O Wi-Fi interno da B13 não funciona no Debian. Se não puder usar o cabo de rede, use um adaptador USB cujo driver exista na sua imagem. Antes de comprar, confira:

```bash
find /lib/modules/$(uname -r) -name '*.ko*' | grep -E 'mt7601u|mt76x0u|mt76x2u|rtw88|rtl8xxxu'
```

Com o cabo de rede ainda ligado, conecte o adaptador e rode:

```bash
apt update
apt install -y firmware-realtek firmware-misc-nonfree network-manager
reboot
```

Depois, confira com `ip link` e conecte com `nmtui`. Se o `apt` não achar os pacotes de firmware, adicione `non-free-firmware` às linhas de `/etc/apt/sources.list`.

O Wi-Fi não substitui o cabo USB do celular: microfone e câmera precisam do `localhost` criado pelo `adb reverse`.

## 10. Trocar o motor de entendimento

O padrão é o Parakeet v3 multilíngue `int8`. Se ele errar muito em português, há duas opções:

- **Whisper:** use `MOTOR_ENTENDIMENTO = "whisper"` no `config.py` e rode `.venv/bin/python ferramentas/baixar_modelos.py`. É mais leve, mas erra mais.
- **Parakeet TAGARELA:** é ajustado para o português do Brasil, mas não tem versão `int8` publicada. Seria preciso gerar essa versão em um computador com bem mais memória e copiar os arquivos para `modelos/parakeet-ptBR`.

## Se der problema

- **`Sem conexão com o computador` na tela:** confira se o terminal mostra `Byte está no ar!`, feche a aba antiga e abra `http://localhost:8000` de novo. Rode `adb reverse --list`. Se estiver vazio, rode `adb reverse tcp:8000 tcp:8000`.
- **`adb devices` mostra `no permissions`:** rode `./ativar_modo_automatico.sh`, depois desconecte e reconecte o cabo.
- **Erro do pip ao instalar as bibliotecas:** algumas bibliotecas podem ainda não ter versão pronta para o Python mais novo do sistema.
- **A tela fica na vertical:** ajuste `user_rotation` em `ferramentas/automatico.py`.
- **`Killed` no log:** a memória acabou. Rode `free -h` e reduza a visão como na seção 7.
- **A bateria do celular cai:** a USB da B13 pode não bastar para a tela sempre ligada. Confira com `adb shell dumpsys battery | grep level`.
- **A câmera não liga:** no Chrome do celular, toque no cadeado ao lado do endereço, em Permissões, e libere a Câmera. Feche outros apps que usam a câmera.
- **A B13 esquenta muito:** deixe-a ventilada e acompanhe com `cat /sys/class/thermal/thermal_zone0/temp`. O valor aparece em milésimos de grau.
