import subprocess
import platform
import re

def escanear_wifi():
    sistema = platform.system()

    if sistema == "Linux":
        # Comando para Linux usando iwlist
        try:
            resultado = subprocess.check_output(["sudo", "iwlist", "scan"], universal_newlines=True)
            redes = parsear_linux_wifi(resultado)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar iwlist: {e}")
            return []
    elif sistema == "Windows":
        # Comando para Windows usando netsh
        try:
            resultado = subprocess.check_output(["netsh", "wlan", "show", "networks"], universal_newlines=True)
            redes = parsear_windows_wifi(resultado)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar netsh: {e}")
            return []
    else:
        print("Sistema operativo no compatible.")
        return []

    return redes

def parsear_linux_wifi(output):
    # Extraer nombres de redes (SSID) y otras características usando expresiones regulares
    redes = []
    celdas = output.split("Cell")  # Divide el escaneo por celdas (una por cada red)
    for celda in celdas[1:]:  # La primera parte no contiene datos útiles
        ssid = re.search(r"ESSID:\"(.+?)\"", celda)
        calidad = re.search(r"Quality=(\d+/\d+)", celda)
        if ssid:
            redes.append({
                "SSID": ssid.group(1),
                "Calidad": calidad.group(1) if calidad else "Desconocida"
            })
    return redes

def parsear_windows_wifi(output):
    # Extraer nombres de redes (SSID) y otras características
    redes = []
    redes_encontradas = re.findall(r"SSID\s\d+\s*:\s(.+)", output)
    calidades = re.findall(r"Signal\s*:\s(\d+)%", output)

    for i, ssid in enumerate(redes_encontradas):
        redes.append({
            "SSID": ssid.strip(),
            "Calidad": f"{calidades[i]}%" if i < len(calidades) else "Desconocida"
        })
    
    return redes

def mostrar_redes(redes):
    if redes:
        print(f"\nSe encontraron {len(redes)} redes WiFi:\n")
        for idx, red in enumerate(redes):
            print(f"{idx + 1}. SSID: {red['SSID']}, Calidad: {red['Calidad']}")
    else:
        print("No se encontraron redes WiFi.")

if __name__ == "__main__":
    print("Escaneando redes WiFi...")
    redes_detectadas = escanear_wifi()
    mostrar_redes(redes_detectadas)
