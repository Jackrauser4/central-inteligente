# MQTT: conceitos

## O que é

**MQTT** (Message Queuing Telemetry Transport) é um protocolo leve de mensagens para comunicação entre dispositivos. Foi criado em 1999 pela IBM para monitorar oleodutos por satélite, onde a conexão era lenta, cara e instável. Por ser muito leve, roda até em microcontroladores como o ESP32. Hoje é um padrão aberto, muito usado em IoT.

## Modelo publicar/assinar (pub/sub)

Em vez de dois programas conversarem diretamente, ambos falam com um intermediário, o **broker**.

```
[Publisher] ──publica──► [Broker] ──entrega──► [Subscriber]
```

- **Broker**: servidor que recebe e distribui as mensagens (aqui, o Mosquitto).
- **Publisher**: quem envia mensagens para um tópico.
- **Subscriber**: quem assina um tópico para receber as mensagens.

Quem publica não sabe quem está ouvindo, e quem ouve não sabe quem publicou. Isso deixa o sistema flexível: dá para adicionar ou trocar componentes sem alterar os outros.

## Tópicos

O tópico é a "categoria" da mensagem, escrito como um caminho separado por `/`:

```
casa/quarto/sensor/ambiente
casa/pc/metricas
```

**Curingas** para assinar vários de uma vez:

| Curinga | Significado | Exemplo |
|---|---|---|
| `#` | Todos os níveis abaixo | `casa/#` recebe tudo que começa com `casa/` |
| `+` | Um único nível | `casa/+/sensor/ambiente` recebe de todos os cômodos |

## Recursos importantes

**Retain (mensagem retida)**
O broker guarda a última mensagem do tópico e a entrega imediatamente a quem assinar depois. Útil para estados (ex.: `online`/`offline`), pois quem chega depois já sabe a situação atual.

**Last Will (última vontade)**
Mensagem cadastrada no broker no momento da conexão. Se o cliente cair sem se despedir, o broker a publica por ele. Usado para avisar que um dispositivo ficou `offline`.

**QoS (qualidade de serviço)**
Define a garantia de entrega:

| Nível | Garantia | Quando usar |
|---|---|---|
| 0 | No máximo uma vez (pode perder) | Leituras frequentes, onde perder uma não importa |
| 1 | Pelo menos uma vez (pode duplicar) | Comandos e eventos importantes |
| 2 | Exatamente uma vez | Casos críticos (mais lento) |

## Ferramentas de teste

```bash
mosquitto_sub -t "casa/#" -v          # escutar tudo
mosquitto_pub -t "casa/teste" -m "oi" # publicar uma mensagem
```

## Convenção usada neste projeto

```
casa/<cômodo>/<tipo>/<nome>        leituras e estados
casa/<cômodo>/<tipo>/<nome>/set    comandos
```

## Onde esse padrão aparece fora de IoT

O modelo pub/sub é a base de sistemas de mensageria usados em backends de grandes empresas, como Kafka, RabbitMQ e Redis Pub/Sub.
