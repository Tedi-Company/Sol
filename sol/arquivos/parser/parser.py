def traduzir(sol_path, lua_path):
    """
    Traduz um arquivo .solscript para Lua.
    Comandos suportados:
    - mostre #texto#
    - crie #ext.nome#
    - abra #ext.nome#  => apenas mostra conteúdo
    - edite #ext.nome# => mostra e permite editar
    """

    with open(sol_path, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    saida = []
    saida.append("-- Gerado automaticamente pelo Sol\n")

    for linha in linhas:
        linha = linha.strip()

        if not linha or linha.startswith("//"):
            continue

        # mostre #texto#
        if linha.startswith("mostre"):
            conteudo = extrair(linha)
            if not conteudo:
                saida.append(f'-- comando inválido: {linha} (use #texto#)\n')
            else:
                saida.append(f'print("{conteudo}")\n')

        # crie #ext.nome#
        elif linha.startswith("crie"):
            conteudo = extrair(linha)
            if not conteudo:
                saida.append(f'-- comando inválido: {linha} (use #ext.nome#)\n')
            else:
                partes = conteudo.split(".", 1)
                if len(partes) == 2:
                    nome_arquivo = f"{partes[1]}.{partes[0]}"
                    saida.append(
f'''
local f = io.open("{nome_arquivo}", "w")
if f then f:close() end
'''
                    )
                else:
                    saida.append(f'-- comando inválido: {linha} (formato errado)\n')

        # abra #ext.nome#  (NÃO MEXIDO)
        elif linha.startswith("abra"):
            conteudo = extrair(linha)
            if not conteudo:
                saida.append(f'-- comando inválido: {linha} (use #ext.nome#)\n')
            else:
                partes = conteudo.split(".", 1)
                if len(partes) == 2:
                    nome_arquivo = f"{partes[1]}.{partes[0]}"
                    saida.append(
f'''
local f = io.open("{nome_arquivo}", "r+")
if not f then
    f = io.open("{nome_arquivo}", "w")
end
if f then
    local conteudo = f:read("*a")
    f:close()
    print("Conteúdo do arquivo:")
    print(conteudo)
end
'''
                    )
                else:
                    saida.append(f'-- comando inválido: {linha} (formato errado)\n')

        # edite #ext.nome#  (NOVO)
        elif linha.startswith("edite"):
            conteudo = extrair(linha)
            if not conteudo:
                saida.append(f'-- comando inválido: {linha} (use #ext.nome#)\n')
            else:
                partes = conteudo.split(".", 1)
                if len(partes) == 2:
                    nome_arquivo = f"{partes[1]}.{partes[0]}"
                    saida.append(
f'''
-- Mostrar conteúdo
local f = io.open("{nome_arquivo}", "r")
local atual = ""
if f then
    atual = f:read("*a")
    f:close()
end

print("Conteúdo atual:")
print(atual)
print("Digite o novo conteúdo (:fim para salvar)")

local linhas = {{}}
while true do
    io.write("> ")
    local l = io.read()
    if l == ":fim" then
        break
    end
    table.insert(linhas, l)
end

local f = io.open("{nome_arquivo}", "w")
if f then
    f:write(table.concat(linhas, "\\n"))
    f:close()
    print("Arquivo salvo.")
end
'''
                    )
                else:
                    saida.append(f'-- comando inválido: {linha} (formato errado)\n')

        # comando desconhecido
        else:
            saida.append(f"-- comando desconhecido: {linha}\n")

    with open(lua_path, "w", encoding="utf-8") as f:
        f.writelines(saida)


def extrair(linha):
    ini = linha.find("#")
    fim = linha.rfind("#")
    if ini != -1 and fim != -1 and fim > ini:
        return linha[ini+1:fim]
    return ""
