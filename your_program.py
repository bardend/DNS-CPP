import subprocess
import sys
import threading
import time

stop_requested = False  # Variable global para detectar la salida

def restore_dns():
    """Restaura la configuración DNS original"""
    print("\n⚠ Restaurando configuración DNS original...")

    new_resolv_conf = """# Configuración de DNS original
nameserver 127.0.0.53
#nameserver 127.0.0.1
options edns0
search .
"""

    try:
        with open("/tmp/resolv.conf", "w") as f:
            f.write(new_resolv_conf)

        subprocess.run(["sudo", "mv", "/tmp/resolv.conf", "/etc/resolv.conf"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "systemd-resolved.service"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "systemd-resolved.service"], check=True)

        print("✅ DNS restaurado correctamente.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error restaurando DNS: {e}")

def stop_systemd_resolved():
    """Detiene y deshabilita systemd-resolved"""
    print("\n🛑 Deteniendo systemd-resolved...")
    commands = [
        ["sudo", "systemctl", "stop", "systemd-resolved"],
        ["sudo", "systemctl", "disable", "systemd-resolved"],
        ["sudo", "rm", "-f", "/etc/resolv.conf"],
    ]
    for cmd in commands:
        subprocess.run(cmd, stderr=subprocess.DEVNULL)

def configure_dns():
    """Configura /etc/resolv.conf manualmente"""
    print("🔧 Configurando /etc/resolv.conf...")

    new_resolv_conf = """# Configuración de DNS modificada por script
#nameserver 127.0.0.53
nameserver 127.0.0.1
options edns0
search .
"""

    with open("/tmp/resolv.conf", "w") as f:
        f.write(new_resolv_conf)

    subprocess.run(["sudo", "mv", "/tmp/resolv.conf", "/etc/resolv.conf"], check=True)
    print("✅ Configuración DNS aplicada.\n")

def cleanup():
    """Elimina contenedor, imagen y restaura DNS"""
    global stop_requested
    if stop_requested:
        return  # Evita múltiples llamadas a cleanup

    stop_requested = True
    print("\n🛑 Se detectó 'X'. Cancelando...")

    print("\n🗑 Eliminando contenedor e imagen Docker...")
    subprocess.run(["docker", "container", "rm", "-f", "dns-server"], stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "image", "rm", "-f", "dns-server:v1"], stderr=subprocess.DEVNULL)

    restore_dns()
    print("🧹 Limpieza completa. ¡Adiós!\n")
    sys.exit(0)

def listen_for_exit():
    """Escucha la entrada del usuario en segundo plano"""
    global stop_requested
    while True:
        choice = input().strip().upper()
        if choice == "X":
            cleanup()
            break

from pyfiglet import Figlet

def run_docker():
    #f = Figlet(font="doh")  # Puedes cambiar el estilo de la fuente
    f = Figlet(font="small")       # Una fuente muy compacta


    print("\n" + "="*70)
    print(f.renderText("DNS SERVER"))
    print("="*70)
    print("\n🚨 PRESIONA 'X' EN CUALQUIER MOMENTO PARA CANCELAR 🚨\n")
    print("="*70)

    time.sleep(3)

    # Iniciar el hilo para escuchar "X"
    listener_thread = threading.Thread(target=listen_for_exit, daemon=True)
    listener_thread.start()

    try:
        print("🐳 Construyendo imagen Docker...")
        subprocess.run(["docker", "image", "build", "-t", "dns-server:v1", "."], check=True)

        print("🚀 Iniciando contenedor DNS...")
        subprocess.run([
            "docker", "container", "run", "--name", "dns-server",
            "-p", "53:53/udp", "-p", "53:53/tcp", "dns-server:v1"
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error en Docker: {e}")
        restore_dns()
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    stop_systemd_resolved()
    configure_dns()
    run_docker()

