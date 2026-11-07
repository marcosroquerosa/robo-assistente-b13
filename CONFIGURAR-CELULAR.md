# Configurar o celular do Robô Byte

O celular é o rosto do robô: mostra a tela, ouve pelo microfone, enxerga pela câmera e fala pelo alto-falante. Ele se liga à B13 por um cabo USB, e a B13 controla o celular pelo **adb** (Android Debug Bridge).

Faça esta configuração **uma vez**, antes de ligar o robô pela primeira vez.

Os nomes dos menus mudam um pouco de uma marca para outra. Quando for diferente, procure pela palavra principal na busca das Configurações (a lupa no topo).

## O que você vai precisar

- Celular Android com o **Chrome** instalado e atualizado.
- **Cabo USB de dados.** Cabo só de carga não serve: o celular carrega, mas a B13 não o enxerga. Na dúvida, use um cabo que você já usou para passar fotos do celular para um computador.

## 1. Ativar as Opções do desenvolvedor

1. Abra **Configurações** › **Sobre o telefone**.
2. Toque **7 vezes seguidas** em **Número da versão** (em alguns celulares, **Número de compilação**).
   - No Motorola: Configurações › Sobre o telefone › **Número da versão**.
   - No Samsung: Configurações › Sobre o telefone › Informações do software › **Número de compilação**.
   - No Xiaomi: Configurações › Sobre o telefone › **Versão do MIUI** (ou **Versão do HyperOS**).
3. Se pedir, digite o PIN ou o desenho de desbloqueio.
4. Aparece a mensagem **"Agora você é um desenvolvedor"**.

As novas opções ficam em **Configurações** › **Sistema** › **Opções do desenvolvedor** (no Samsung, no fim da lista das Configurações).

## 2. Ligar a depuração USB

Em **Opções do desenvolvedor**:

1. Ative **Depuração USB** e confirme.
2. Ative **Permanecer ativo** (a tela não apaga enquanto carrega).
3. No Xiaomi, ative também **Depuração USB (configurações de segurança)**.

## 3. Autorizar a B13

1. Ligue o celular na B13 pelo cabo.
2. No celular aparece a pergunta **"Permitir depuração USB?"**.
3. Marque **"Sempre permitir deste computador"** e toque em **Permitir**.

Confira na B13:

```bash
adb devices
```

Deve aparecer um código seguido da palavra `device`:

```
List of devices attached
ZY22ABCDEF    device
```

| O que aparece | O que fazer |
| --- | --- |
| `device` | Pronto. Siga para o passo 4. |
| `unauthorized` | Falta aceitar a pergunta no celular. Desbloqueie a tela e procure o aviso. |
| `no permissions` | Rode as permissões do USB (veja "Se der problema"). |
| Lista vazia | A B13 não está vendo o celular. Veja "Se der problema". |

Se o aviso não aparecer, puxe a barra de notificações, toque na notificação do USB e escolha **Transferência de arquivos**.

## 4. Deixar o celular pronto para ficar ligado o tempo todo

O robô fica de pé o dia inteiro, sem ninguém mexer no celular.

| Onde | O que mudar | Por quê |
| --- | --- | --- |
| Configurações › Segurança › Bloqueio de tela | **Nenhum** | Para o robô voltar sozinho depois de reiniciar |
| Configurações › Bateria › Uso da bateria do app › **Chrome** | **Sem restrições** | Para o Android não fechar o rosto do robô |
| Configurações › Som | Volume de **mídia** alto | A voz do robô sai pelo volume de mídia |
| Configurações › Notificações | **Não perturbe** desligado, ou com mídia liberada | Para o robô não ficar mudo |
| Play Store › foto do perfil › Configurações › Rede | Atualização automática **só pelo Wi-Fi**, ou desligada | Para o Chrome não reiniciar no meio da aula |

A rotação da tela e o tempo de tela ligada são controlados pela B13 quando o modo automático está ativo. Não precisa mudar isso à mão.

## 5. Liberar o microfone e a câmera no Chrome

1. Na B13, ligue o robô com `./iniciar.sh` e espere `Byte está no ar!`.
2. No Chrome do celular, abra **`http://localhost:8000`**.
3. Toque na tela e permita o **microfone** e a **câmera**. Se o Chrome perguntar, escolha **"Permitir sempre"** (ou **"Ao usar o site"**).

O endereço tem que ser exatamente `localhost`. O Chrome só libera microfone e câmera em `localhost` ou em sites com HTTPS. O `iniciar.sh` cria esse caminho pelo cabo com o comando `adb reverse`.

Se você negou sem querer: no Chrome, toque no ícone ao lado do endereço › **Permissões** e libere o Microfone e a Câmera. Depois recarregue a página.

## Lista de conferência

- [ ] Opções do desenvolvedor ativadas
- [ ] Depuração USB ligada
- [ ] Permanecer ativo ligado
- [ ] B13 autorizada com "Sempre permitir deste computador"
- [ ] `adb devices` mostra `device`
- [ ] Bloqueio de tela em "Nenhum"
- [ ] Chrome sem restrição de bateria
- [ ] Volume de mídia alto
- [ ] Microfone e câmera permitidos em `http://localhost:8000`

## Se der problema

**`adb devices` vem vazio ou mostra `no permissions`**

Instale na B13 as permissões do USB para celulares Android de qualquer fabricante (o `instalar.sh` da v1.1 já faz isso):

```bash
apt install -y android-sdk-platform-tools-common
udevadm control --reload-rules
udevadm trigger
```

Depois, desconecte e reconecte o cabo e confira com `adb kill-server && adb devices`.

Se continuar vazio, rode `lsusb` com o celular plugado:

- **O celular não aparece na lista:** o problema é o cabo ou a porta. Troque por um cabo de dados e teste a outra porta USB da B13.
- **O celular aparece:** o problema é a configuração do celular. Em Opções do desenvolvedor, toque em **Revogar autorizações de depuração USB**, desligue e ligue a Depuração USB, reconecte o cabo e aceite o aviso de novo.

**O celular estava autorizado em outro computador**

A autorização vale para cada computador. Se o celular já foi usado com o NucBox ou com um PC, ele precisa autorizar a B13 também (passo 3).

**A página não abre no celular (`Sem conexão com o computador`)**

Na B13, rode `adb reverse --list`. Se estiver vazio:

```bash
adb reverse tcp:8000 tcp:8000
```

**A bateria do celular cai mesmo ligado no cabo**

A porta USB da B13 fornece pouca energia, e a tela sempre ligada gasta bastante. Baixe o brilho da tela e acompanhe com:

```bash
adb shell dumpsys battery | grep level
```

Se continuar caindo, use o plano B abaixo, com o celular no carregador próprio.

## Plano B: ligação sem cabo (Depuração por Wi-Fi)

Funciona em Android 11 ou mais novo. O celular precisa estar no Wi-Fi da **mesma rede** em que a B13 está ligada pelo cabo de rede. O `adb reverse` funciona igual, então o endereço continua sendo `http://localhost:8000`.

1. Em Opções do desenvolvedor, ative **Depuração por Wi-Fi** e toque no nome da opção para abrir.
2. Toque em **Parear dispositivo com código de pareamento**. Aparecem um IP, uma porta e um código de 6 dígitos.
3. Na B13, use o IP e a porta dessa tela e digite o código quando pedir:
   ```bash
   adb pair 192.168.0.30:37115
   ```
4. Volte à tela principal da Depuração por Wi-Fi. Ela mostra **outro** IP e porta. Conecte com eles:
   ```bash
   adb connect 192.168.0.30:41023
   adb reverse tcp:8000 tcp:8000
   ```
5. Deixe o celular no carregador próprio.

A porta muda quando o celular reinicia ou quando a Depuração por Wi-Fi é desligada. Nesse caso, repita o passo 4.

## Cuidados

- **Bateria:** o celular fica carregando o tempo todo. Deixe ventilação atrás dele e veja de vez em quando se a bateria não está estufando.
- **Segurança:** com a depuração USB ligada, quem tiver acesso à B13 controla o celular. Use um celular só para o robô, sem contas pessoais nem dados de alunos.
