import re
import textwrap

# Função para gerar o slug (URL amigável)
def gerar_slug(palavra):
    slug = re.sub(r'[áàãâä]', 'a', palavra.lower())
    slug = re.sub(r'[éèêë]', 'e', slug)
    slug = re.sub(r'[íìîï]', 'i', slug)
    slug = re.sub(r'[óòõôö]', 'o', slug)
    slug = re.sub(r'[úùûü]', 'u', slug)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')

# Função para formatar o texto
def formatar_texto(texto, palavra_chave=None):
    # Tenta inferir palavra-chave se não for informada
    if not palavra_chave:
        primeira_linha = texto.strip().split('\n')[0]
        palavra_chave = primeira_linha.strip()

    slug = gerar_slug(palavra_chave)

    # Bloco inicial
    title = f"{palavra_chave.capitalize()}: guia completo para SEO"
    if len(title) < 50:
        title += " e boas práticas"
    title = title[:60]

    description = f"{palavra_chave.capitalize()} é o foco deste conteúdo. Descubra tudo sobre o tema, sua importância e como aplicar de forma estratégica no SEO."
    description = description[:160]

    bloco_inicial = textwrap.dedent(f"""
    **Title:** {title}

    **Description:** {description}

    **URL amigável:** {slug}

    **H1:** {palavra_chave.capitalize()}
    """)

    # Linha divisória
    resultado = bloco_inicial + "\n________________\n\n"

    # Aplicar marcações H2 / H3
    linhas = texto.split("\n")
    for i, linha in enumerate(linhas):
        linha_limpa = linha.strip()
        if re.match(r'^\s*$', linha_limpa):
            resultado += "\n"
        elif linha_limpa.startswith("•") or linha_limpa.startswith("*"):
            linha_limpa = linha_limpa.replace("•", "*").strip()
            if not linha_limpa.endswith(('.', ';')):
                linha_limpa += ";"
            resultado += f"{linha_limpa}\n"
        elif linha_limpa.lower().startswith(("h2:", "h3:")):
            resultado += f"**{linha_limpa.strip()}**\n\n"
        elif linha_limpa.lower().startswith(("o que é", "como", "quanto", "por que")):
            resultado += f"**H2: {linha_limpa.strip()}?**\n\n"
        else:
            resultado += linha_limpa + "\n\n"

    return resultado.strip()


# Execução direta no terminal
if __name__ == "__main__":
    print("📄 Bem-vinda ao SEO Text Formatter\n")
    entrada = input("Digite o nome do arquivo de texto original (ex: texto.txt): ")
    saida = input("Digite o nome do arquivo de saída (ex: texto_formatado.txt): ")
    palavra_chave = input("Informe a palavra-chave principal (ou deixe vazio para detectar): ").strip() or None

    try:
        with open(entrada, "r", encoding="utf-8") as f:
            texto_original = f.read()

        texto_formatado = formatar_texto(texto_original, palavra_chave)

        with open(saida, "w", encoding="utf-8") as f:
            f.write(texto_formatado)

        print(f"\n✅ Texto formatado com sucesso! Arquivo salvo como: {saida}")

    except FileNotFoundError:
        print("\n❌ Arquivo de entrada não encontrado. Verifique o nome e tente novamente.")
