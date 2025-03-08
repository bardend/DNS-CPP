import subprocess
import sys
import time
import signal



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

from pyfiglet import Figlet

def run_docker():
    f = Figlet(font="small")
    print("\n" + "="*70)
    print(f.renderText("DNS SERVER"))
    print("="*70)
    process = subprocess.Popen(
        ["docker-compose", "up", "--build"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # Maneja Ctrl+C para limpiar antes de salir
    def signal_handler(sig, frame):
        print("\nDeteniendo contenedores... HABER")
        subprocess.run(["docker-compose", "down"], check=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Espera a que el usuario presione una tecla
    print("\nPresiona ENTER para detener el servidor y limpiar...")
    input()

    # Detiene los contenedores al presionar ENTER
    subprocess.run(["docker-compose", "down"], check=True)
    restore_dns()
    print("Deteniendo contenedores...")


if __name__ == "__main__":
    stop_systemd_resolved()
    configure_dns()
    run_docker()

