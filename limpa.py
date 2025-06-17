import subprocess
import sys

def run_command(cmd):
    """Executa comando shell e exibe saída"""
    print(f"Executando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro: {result.stderr.strip()}")
        sys.exit(result.returncode)
    print(result.stdout.strip())

def main():
    # Desinstalar python-telegram-bot
    run_command("pip uninstall python-telegram-bot -y")

    # Instalar versão 20.8
    run_command("pip install python-telegram-bot==20.8")

    # Rodar main.py
    run_command(f"{sys.executable} main.py")

if __name__ == "__main__":
    main()
