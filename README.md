# Robô Byte na BTV B13

Robô de mesa que ajuda em aulas de informática. Ele ouve uma pergunta, entende, pensa e responde falando, em português do Brasil.

Esta é a versão do Byte para a TV box **BTV B13** com Debian 13, adaptada do projeto original [robo-assistente](https://github.com/marcosroquerosa/robo-assistente), feito para o NucBox5. A B13 faz o trabalho do computador, e um celular reaproveitado funciona como rosto.

A voz, o entendimento da fala e o reconhecimento de rostos rodam na própria B13, sem internet. A internet é usada para a IA que pensa nas respostas e para buscar imagens.

![Foto do Robô Byte na BTV B13](foto-robo-b13.jpg)

## O que ele faz

- **Conversa por voz:** acorda com "ei robô" ou com um toque na tela, responde em voz alta e mostra legendas.
- **Reconhece pessoas:** aprende rostos, cumprimenta pelo nome e sabe quem está na frente da câmera.
- **Enxerga:** tira fotos, descreve o que vê e lê o quadro.
- **Mostra imagens:** busca na Wikipédia e no Wikimedia Commons, confere com a IA e explica para a turma.
- **Tem expressões:** mostra alegria, dúvida, surpresa e sono.
- **Usa a tela para ensinar:** mostra listas, passos e textos enquanto fala.
- **Presta atenção:** olha para quem está falando e percebe uma mão levantada pedindo a vez.

A lista completa de frases está em [COMANDOS-ROBO-BYTE.md](COMANDOS-ROBO-BYTE.md).

## Como funciona

![Arquitetura do robô na B13](arquitetura-robo.png)

O celular é a interface: mostra o rosto e cuida do microfone, da câmera e do alto-falante. A B13 faz o trabalho pesado e não precisa de tela depois de configurada.

## Equipamentos

| Aparelho | Modelo | Papel no robô |
| --- | --- | --- |
| TV box | BTV B13 (Amlogic S905X4, 4 núcleos, 2 GB de memória, 16 GB internos) | O "cérebro": roda o programa do robô e os modelos locais |
| Celular | Android com Chrome e depuração USB | O "rosto": tela, microfone, câmera frontal e alto-falante |
| Cabo USB | De dados, ligado à porta USB da B13 | Leva os dados entre os dois e abre o `localhost` no celular |
| Rede | Cabo de rede, ou adaptador Wi-Fi USB compatível | Dá acesso à internet para a IA e as imagens |

No Debian, o Wi-Fi interno, o Bluetooth interno e o som pelo HDMI da B13 não funcionam. O robô não depende deles: o som sai do celular, e a rede pode ser por cabo ou por um adaptador USB.

## O que muda em relação ao projeto original

| Parte | NucBox5 | BTV B13 |
| --- | --- | --- |
| Sistema | Lubuntu | Debian 13 na memória interna, sem Android |
| Entendimento | Parakeet TAGARELA completo | Parakeet TDT 0.6B v3 multilíngue `int8`, por causa dos 2 GB de memória |
| Cérebro | Gemini, com Ollama como reserva | Só Gemini. Sem internet, o robô avisa que não consegue responder |
| Visão | 640 px, até 4 imagens por segundo em grupo | 480 px e 2 imagens por segundo |
| Duração da fala | Até 100 segundos | Até 25 segundos por vez |

## Tecnologias

| Parte do robô | Tecnologia | O que faz | Onde roda | Precisa de internet? |
| --- | --- | --- | --- | --- |
| Sistema operacional | Debian 13 | Base que roda tudo | B13 | Não |
| Linguagem | Python | Programa do robô | B13 | Não |
| Ponte com o celular | FastAPI e Uvicorn | Entrega a página do rosto e troca mensagens por WebSocket | B13 | Não |
| Cabo de dados | adb (Android Debug Bridge) | Faz o celular enxergar o robô pelo cabo e controla a tela | B13 e celular | Não |
| Rosto | HTML, CSS, JavaScript e Canvas 2D no Chrome | Desenha o rosto, mostra cartões e legendas, grava o som e toca a voz | Celular | Não |
| Palavra de ativação | Vosk | Fica atento às palavras de ativação, gastando pouco | B13 | Não |
| Entendimento | Parakeet TDT 0.6B v3 `int8`, pelo onnx-asr | Transforma a fala em texto | B13 | Não |
| Entendimento alternativo | Whisper (faster-whisper) | Faz a mesma tarefa, se for escolhido no `config.py` | B13 | Não |
| Cérebro | Google Gemini, por API compatível com OpenAI | Pensa na resposta e analisa fotos | Internet | Sim |
| Voz | Piper, voz "faber" | Transforma a resposta em fala | B13 | Não |
| Rostos | OpenCV, YuNet e SFace | Acha e reconhece rostos | B13 | Não |
| Mãos | Detector de palmas do OpenCV Zoo, pelo onnxruntime | Percebe a mão levantada | B13 | Não |
| Imagens | API da Wikipédia e do Wikimedia Commons | Busca imagens livres para a aula | Internet | Sim |
| Início automático | systemd (serviço `robo-byte`) | Liga o robô com a B13 e religa se cair | B13 | Não |

## Instalação

Primeiro, instale o Debian na B13 com o [tutorial do projeto gabclima/b13](https://github.com/gabclima/b13/blob/main/TUTORIAL.md). **Esse processo apaga o Android**, e o tutorial exige um backup antes. Depois, como `root`:

```bash
apt install -y git
cd /root
git clone https://github.com/marcosroquerosa/robo-assistente-b13
cd robo-assistente-b13
bash instalar.sh
```

O instalador coloca os programas, as bibliotecas e os modelos.

Crie uma chave no Google AI Studio e salve no arquivo `chave_web.txt`, na pasta do projeto. Esta versão precisa da chave para conversar.

Para buscar imagens, coloque seu e-mail em `IMAGENS_CONTATO`, em `robo/config.py`. A Wikipédia e o Commons exigem um contato de quem usa a busca.

O passo a passo completo está em [LEIA-ME-B13.md](LEIA-ME-B13.md).

## Como usar

**Para testar:** ligue o celular no cabo, rode o comando abaixo e abra `http://localhost:8000` no Chrome do celular. Depois, toque na tela e permita o microfone e a câmera.

```bash
./iniciar.sh
```

O endereço precisa ser `localhost`, porque o Chrome só libera microfone e câmera em HTTPS ou em `localhost`. O cabo com `adb reverse` resolve isso.

**Para ligar sozinho com a B13:**

```bash
./ativar_modo_automatico.sh
```

## O caminho de uma pergunta

1. **Dormindo:** o Vosk procura a palavra de ativação. Tocar na tela também acorda o robô.
2. **Ouvindo:** o robô grava a pergunta até a pessoa ficar 1 segundo em silêncio.
3. **Pensando:** o Parakeet transforma a gravação em texto. Pedidos como "tira uma foto" são resolvidos na hora, e o restante vai para o Gemini.
4. **Falando:** cada frase vira áudio no Piper. Enquanto o celular fala uma frase, a B13 prepara a próxima.

Depois de falar, o robô espera outra pergunta por 4 segundos, sem precisar da palavra de ativação. Enquanto pensa e fala, ele não escuta, para não confundir a própria voz com a de alguém.

## Modo automático

Depois de ativado, basta ligar a B13 na tomada. O serviço `robo-byte` roda o `ferramentas/automatico.py`, que:

- liga o servidor do robô e espera os modelos carregarem;
- quando o celular aparece no cabo, abre o caminho com `adb reverse`, mantém a tela ligada, deixa na horizontal, abre o rosto no Chrome e toca na tela para liberar o som;
- religa o robô se ele cair e prepara o celular de novo se o cabo sair e voltar.

Alguns ajustes são feitos à mão, uma vez:

- **Depuração USB:** ligada no celular, com "Sempre permitir deste computador".
- **Celular:** bloqueio de tela "Nenhum", com microfone e câmera permitidos no Chrome.

## Estrutura do projeto

```text
robo-assistente-b13/
├── robo/                       programa do robô (B13)
│   ├── config.py               painel de controle
│   ├── personalidade.txt       jeito de ser do robô
│   ├── servidor.py             ponte com o celular
│   ├── robo.py                 sistema nervoso: liga as partes
│   ├── ouvido.py               palavra de ativação e gravação
│   ├── transcricao.py          fala vira texto
│   ├── comandos.py             pedidos resolvidos sem a IA
│   ├── cerebro.py              pensa na resposta
│   ├── marcas.py               expressões e cartões pedidos pela IA
│   ├── voz.py                  texto vira fala
│   ├── visao.py                acha rostos e mãos e reconhece pessoas
│   ├── atencao.py              descobre quem fala e quem pede a vez
│   └── imagens.py              busca na Wikipédia e no Commons
├── rosto/                      página que abre no celular
├── ferramentas/
│   ├── automatico.py           piloto automático
│   ├── baixar_modelos.py       baixa os modelos
│   └── rostos.py               lista, renomeia e apaga rostos
├── instalar.sh                 instala tudo
├── iniciar.sh                  liga o robô à mão
├── ativar_modo_automatico.sh   liga sozinho com a B13
├── desativar_modo_automatico.sh
├── requirements.txt            bibliotecas Python
├── COMANDOS-ROBO-BYTE.md       tudo o que o robô entende
└── LEIA-ME-B13.md              guia de instalação e uso
```

Estes itens são criados na instalação ou no uso e não devem ir para o repositório: `chave_web.txt`, `.venv/`, `modelos/`, `dados/` e `fotos/`. O `.gitignore` já cuida disso.

## Configurações principais

Os ajustes ficam em `robo/config.py`. Depois de mudar, reinicie o robô com `systemctl restart robo-byte`.

| Ajuste | Valor padrão | Para que serve |
| --- | --- | --- |
| `PALAVRAS_DE_ATIVACAO` | "ei robô", "oi byte" e outras | Frases que acordam o robô |
| `MOTOR_ENTENDIMENTO` | `parakeet` | Quem transforma fala em texto: `parakeet` ou `whisper` |
| `PARAKEET_QUANTIZACAO` | `int8` | Versão compacta do Parakeet |
| `WEB_MODELO` | `gemini-3.5-flash-lite` | Qual IA da web usar |
| `TAMANHO_MAXIMO_DA_RESPOSTA` | 380 | Limite da resposta, em tokens |
| `CRIATIVIDADE` | 0,3 | Mais baixo deixa as respostas mais diretas |
| `LIMIAR_DE_SILENCIO` | 600 | Quanto barulho conta como fala |
| `SEGUNDOS_DE_SILENCIO_PARA_PARAR` | 1 | Pausa que encerra a pergunta |
| `SEGUNDOS_ESPERANDO_PERGUNTA` | 4 | Tempo de espera por uma pergunta |
| `SEGUNDOS_MAXIMOS_DE_FALA` | 25 | Duração máxima de uma pergunta |
| `IMAGENS_FONTES` | `wikipedia`, `commons` | Onde buscar imagens |
| `VISAO_LARGURA_DO_QUADRO` | 480 | Tamanho das imagens da câmera; 320 pesa menos |
| `VISAO_QUADROS_POR_SEGUNDO` | 2 | Imagens por segundo; abaixo disso, mão levantada e olhar para quem fala falham |
| `VISAO_OLHAR_QUEM_FALA` | `True` | Liga o olhar para quem está falando |
| `VISAO_MAO_LEVANTADA` | `True` | Liga a detecção da mão levantada |
| `ROSTO_IA_ESCOLHE_EXPRESSAO` | `True` | Deixa a IA da web escolher as expressões |
| `TELA_IA_PODE_MOSTRAR` | `True` | Deixa a IA da web mostrar cartões na tela |

Para mudar o jeito do robô, edite `robo/personalidade.txt`.

## Comandos úteis

Rode como `root`, na pasta do projeto.

| Para | Comando |
| --- | --- |
| Ver o que o robô está fazendo | `journalctl -u robo-byte -f` |
| Ver só o que ele ouviu e os tempos | `journalctl -u robo-byte -f \| grep -E "ouvi:\|tempo"` |
| Saber se o robô está rodando | `systemctl status robo-byte` |
| Reiniciar o robô | `systemctl restart robo-byte` |
| Parar até o próximo reinício | `systemctl stop robo-byte` |
| Conferir o celular no cabo | `adb devices` |
| Ver a memória livre | `free -h` |
| Ver a temperatura, em milésimos de grau | `cat /sys/class/thermal/thermal_zone0/temp` |
| Ver a bateria do celular | `adb shell dumpsys battery \| grep level` |
| Desligar o modo automático | `./desativar_modo_automatico.sh` |
| Conversar pelo teclado | `.venv/bin/python -m robo.cerebro` |
| Testar a voz | `.venv/bin/python -m robo.voz` |
| Ver qual comando uma frase vira | `.venv/bin/python -m robo.comandos` |
| Ver rostos e mãos numa foto | `.venv/bin/python -m robo.visao foto.jpg` |
| Testar a busca de imagens | `.venv/bin/python -m robo.imagens placa-mãe` |
| Ver quem o robô conhece | `.venv/bin/python ferramentas/rostos.py listar` |

## Privacidade

- **Áudio:** nunca sai da B13 e não é gravado em arquivo.
- **Texto:** o texto das perguntas vai para o Google. Os nomes das pessoas reconhecidas também vão, a menos que `VISAO_CONTAR_NOMES_PARA_IA` seja `False`.
- **Câmera:** o reconhecimento roda na B13. Uma foto só vai para a IA da web quando alguém pede para o robô olhar, e a tela mostra um aviso.
- **Rostos:** `dados/rostos.json` guarda assinaturas numéricas, não fotos. Rosto é dado biométrico sensível, então peça autorização dos responsáveis e da escola antes de cadastrar alunos.
- **Imagens:** as buscas vão para a Wikipédia e o Commons, com o contato de `IMAGENS_CONTATO`. As imagens não são gravadas em disco.
- **Memória:** a conversa fica só na memória e some quando o robô reinicia. As fotos de "tira uma foto" ficam em `fotos/`.

Avise a turma e a escola de que o robô escuta e usa uma câmera.

## Créditos

- [robo-assistente](https://github.com/marcosroquerosa/robo-assistente): projeto original do Robô Byte.
- [gabclima/b13](https://github.com/gabclima/b13): instalação do Debian na memória interna da BTV B13.
- [devmfc/debian-on-amlogic](https://github.com/devmfc/debian-on-amlogic): imagem do Debian para Amlogic.
- [istupakov/onnx-asr](https://github.com/istupakov/onnx-asr): execução do Parakeet em ONNX.
