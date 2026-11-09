# Central Inteligente

Central de automação residencial desenvolvida do zero: painel web, backend, banco de dados e integrações próprias, sem depender de plataformas prontas como cérebro do sistema. O projeto começa pelo quarto e vai se expandir para a casa toda.

## Objetivo

- Painel com relógio, temperatura e umidade do ambiente e clima externo
- Monitoramento do PC (CPU, RAM, GPU, VRAM, discos)
- Monitoramento da rede Wi-Fi
- Controle de iluminação e áudio
- Sensores, segurança e automações (modos Cinema, Estudo, Dormir, Ausente e Gaming)

## Arquitetura

```
[Agente Python]──┐
[ESP32 sensores]─┼─► [Mosquitto MQTT] ─► [Backend] ─► [PostgreSQL]
[Open-Meteo API]─┘                          │
                                            └─► WebSocket ─► [Painel web]
```

Todos os componentes conversam por **MQTT** (publish/subscribe) através de um broker central. Isso permite adicionar ou trocar partes sem mexer nas outras.

## Convenção de tópicos MQTT

```
casa/<cômodo>/<tipo>/<nome>        leituras e estados
casa/<cômodo>/<tipo>/<nome>/set    comandos
```

Tópicos em uso hoje:

| Tópico | Conteúdo |
|---|---|
| `casa/pc/metricas` | JSON com cpu, cpu_temp, ram, gpu, gpu_temp, vram, disco |
| `casa/pc/status` | `online` / `offline` (retido, com Last Will) |

## Tecnologias

| Tecnologia | Uso |
|---|---|
| MQTT (Mosquitto) | Comunicação entre os componentes |
| Python | Agente de monitoramento do PC |
| Ubuntu | Sistema onde o projeto roda |
| (planejado) Backend, PostgreSQL, ESP32 em C++ | Próximas etapas |

## Progresso

- [x] **Etapa 1**: Mosquitto + agente Python publicando métricas do PC
- [ ] Etapa 2: backend assinando o MQTT e enviando dados por WebSocket
- [ ] Etapa 3: painel web em tempo real
- [ ] Etapa 4: banco de dados e histórico
- [ ] Etapa 5: monitoramento da rede
- [ ] Etapa 6: primeiro ESP32 com sensor de temperatura e umidade
- [ ] Etapa 7: iluminação e áudio
- [ ] Etapa 8: automações
- [ ] Etapa 9: servidor dedicado
- [ ] Etapa 10: tela touchscreen na parede

## Como rodar (etapa 1)

```bash
# broker
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto

# agente
cd agente-pc
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python agente_pc.py
```

Para ver os dados chegando:

```bash
mosquitto_sub -t "casa/#" -v
```

## Documentação

As notas de cada etapa ficam na pasta [docs](docs/).
