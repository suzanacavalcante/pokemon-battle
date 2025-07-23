import datetime

# Mensagem que será exibida na página HTML
mensagem_do_python = "Olá do Python!"
data_geracao_atual = datetime.datetime.now().isoformat()

# Conteúdo HTML que será escrito no arquivo index.html
# Inclui um botão que simplesmente recarrega a página
html_content = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mensagem Atualizada do Python</title>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f2f5;
            color: #333;
        }}
        .container {{
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 20px;
        }}
        mensagem-container {{
            font-size: 1.2em;
            margin-bottom: 30px;
            padding: 15px;
            background-color: #e8f5e9;
            border-radius: 10px;
            border: 1px solid #c8e6c9;
            color: #2e7d32;
        }}
        button {{
            background-color: #4CAF50;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
        button:hover {{
            background-color: #45a049;
            transform: translateY(-2px);
        }}
        button:active {{
            transform: translateY(0);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Mensagem:</h1>
        <div id="mensagem-container">
            {mensagem_do_python} (Gerado em: {data_geracao_atual})
        </div>
        <button onclick="location.reload()">Atualizar Mensagem</button>
        <p style="margin-top: 20px; font-size: 0.85em; color: #777;">
            Para ver uma nova mensagem, execute o script Python novamente no seu terminal e depois clique em 'Atualizar Mensagem'.
        </p>
    </div>
</body>
</html>
"""

# Nome do arquivo HTML de saída
nome_arquivo_html = 'index.html'

# Escreve o conteúdo HTML no arquivo
with open(nome_arquivo_html, 'w', encoding='utf-8') as arquivo:
    arquivo.write(html_content)

print(f"Página HTML '{nome_arquivo_html}' gerada/atualizada com sucesso.")
