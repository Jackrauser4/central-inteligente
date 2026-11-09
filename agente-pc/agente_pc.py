import json, time
import psutil, pynvml
import paho.mqtt.client as mqtt

pynvml.nvmlInit()
gpu = pynvml.nvmlDeviceGetHandleByIndex(0)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.will_set("casa/pc/status", "offline", retain=True)
client.connect("localhost", 1883)
client.loop_start()
client.publish("casa/pc/status", "online", retain=True)

def temp_cpu():
    temps = psutil.sensors_temperatures()
    for nome in ("coretemp", "k10temp"):
        if nome in temps:
            return temps[nome][0].current
    return None

psutil.cpu_percent(interval=None)

while True:
    mem = pynvml.nvmlDeviceGetMemoryInfo(gpu)
    dados = {
        "cpu": psutil.cpu_percent(interval=None),
        "cpu_temp": temp_cpu(),
        "ram": psutil.virtual_memory().percent,
        "gpu": pynvml.nvmlDeviceGetUtilizationRates(gpu).gpu,
        "gpu_temp": pynvml.nvmlDeviceGetTemperature(gpu, pynvml.NVML_TEMPERATURE_GPU),
        "vram": round(mem.used / mem.total * 100, 1),
        "disco": psutil.disk_usage("/").percent,
    }
    client.publish("casa/pc/metricas", json.dumps(dados))
    time.sleep(2)


