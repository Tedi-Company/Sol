import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parser.parser import traduzir

def base_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def executar_lua(script_lua):
    base = base_path()
    lua_exe = os.path.join(base, "lua", "lua.exe")
    if not os.path.exists(lua_exe):
        print("Erro: lua.exe não encontrado")
        sys.exit(1)
    subprocess.run([lua_exe, script_lua])

def executar_solscript(arquivo_solscript):
    base = base_path()
    cache_dir = os.path.join(base, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    lua_saida = os.path.join(cache_dir, "script.lua")

    traduzir(arquivo_solscript, lua_saida)
    executar_lua(lua_saida)

def terminal():
    print("Bem-vindo ao terminal da linguagem Sol! Digite 'sair' para encerrar. Se aparecer ... na tela clique em enter.")
    base = base_path()
    cache_dir = os.path.join(base, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    lua_saida = os.path.join(cache_dir, "terminal.lua")

    buffer = ""
    while True:
        try:
            prompt = "... " if buffer else ">>> "
            comando = input(prompt)

            if comando.lower() in ("sair", "exit", "quit"):
                break

            # termina bloco com 'fim' ou linha vazia
            if comando.strip() == "fim" or (buffer and comando.strip() == ""):
                if buffer:
                    temp_solscript = os.path.join(cache_dir, "temp.solscript")
                    with open(temp_solscript, "w", encoding="utf-8") as f:
                        f.write(buffer)
                    traduzir(temp_solscript, lua_saida)
                    executar_lua(lua_saida)
                    os.remove(temp_solscript)
                    buffer = ""
                continue
            else:
                if buffer:
                    buffer += "\n" + comando
                else:
                    buffer = comando
        except Exception as e:
            print(f"Erro: {e}")

def main():
    # Detecta clique duplo ou execução via terminal
    if len(sys.argv) == 1:
        terminal()
    else:
        arquivo = sys.argv[1]
        if not arquivo.endswith(".solscript"):
            print("Erro: arquivo não é .solscript")
            sys.exit(1)
        if not os.path.exists(arquivo):
            print(f"Erro: arquivo {arquivo} não encontrado")
            sys.exit(1)
        executar_solscript(arquivo)

if __name__ == "__main__":
    main()
