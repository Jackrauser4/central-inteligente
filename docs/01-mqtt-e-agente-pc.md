# Etapa 1: MQTT e agente de monitoramento do PC

## Objetivo

Montar a base de comunicação do projeto: um broker MQTT e um primeiro programa que publica dados reais (métricas do PC) para qualquer outro componente consumir.

## Conceitos

**MQTT** (Message Queuing Telemetry Transport) é um protocolo leve de mensagens, criado em 1999 pela IBM para monitorar oleodutos por conexões instáveis. Funciona no modelo publicar/assinar.

- **Broker**: o servidor que recebe e distribui as mensagens (Mosquitto).
- **Publisher**: quem publica numa categoria (o agente Python).
- **Subscriber**: quem assina uma categoria para receber as mensagens (`mosquitto_sub`, e em breve o backend).
- **Tópico**: a categoria, escrita como caminho, por exemplo `casa/pc/metricas`.
- **Curinga `#`**: `casa/#` significa tudo que começa com `casa/`.
- **Retain**: o broker guarda a última mensagem do tópico e entrega a quem assinar depois.
- **Last Will**: mensagem de despedida cadastrada no broker; se o cliente cair sem avisar, o broker a publica por ele (usado para o status `offline`).

Quem publica não sabe quem ouve, e quem ouve não sabe quem publicou. Por isso os componentes podem ser trocados ou adicionados sem alterar os outros.

## O que foi feito

1. Instalação do Mosquitto no Ubuntu e teste com `mosquitto_pub` e `mosquitto_sub`.
2. Criação de um ambiente virtual Python e instalação de `psutil`, `paho-mqtt` e `nvidia-ml-py`.
3. Criação do agente `agente-pc/agente_pc.py`, que lê CPU, temperatura da CPU, RAM, GPU, temperatura da GPU, VRAM e disco, e publica um JSON em `casa/pc/metricas` a cada 2 segundos.
4. Publicação do status `online` em `casa/pc/status`, com Last Will `offline`.
5. Versionamento no Git e envio ao GitHub por SSH.

## Como rodar

```bash
cd agente-pc
source venv/bin/activate
python agente_pc.py
```

Em outro terminal:

```bash
mosquitto_sub -t "casa/#" -v
```

## Decisões

- **Ambiente virtual**: o Ubuntu recente bloqueia `pip install` global; o venv isola as dependências do projeto.
- **JSON nas mensagens**: formato que qualquer linguagem lê, o que permite backend em outra linguagem.
- **Temperatura da CPU via psutil**: no Linux o sensor se chama `coretemp` (Intel) ou `k10temp` (AMD).
- **Tópicos hierárquicos**: padrão `casa/<cômodo>/<tipo>/<nome>` para não precisar renomear nada quando entrarem luzes e áudio.

## Problemas e soluções

| Problema | Causa | Solução |
|---|---|---|
| `Command 'pip' not found` | Ambiente virtual não estava ativo | `source venv/bin/activate` |
| `key ... marked as read only` no `git push` | Chave SSH cadastrada como deploy key, sem escrita | Cadastrar a chave em Settings → SSH and GPG keys da conta |
| `systemctl status` preso na tela | Modo de paginação | Apertar `q` |

## Próxima etapa

Backend assinando `casa/pc/metricas` e enviando os dados ao painel por WebSocket.
