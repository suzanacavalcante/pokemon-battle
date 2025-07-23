import pandas as pd
import datetime
import json
import ast # Importar a biblioteca ast para ast.literal_eval

# --- Configurações ---
# Nome do arquivo CSV com os dados dos Pokémon
POKEMON_CSV_FILE = 'final_pokemon.csv'
# Nome do arquivo HTML de saída
OUTPUT_HTML_FILE = 'index.html'
# Número de Pokémon a serem exibidos na tabela (para começar, vamos limitar em 20)
NUM_POKEMON_TO_SHOW = 800

# --- Funções Auxiliares ---
def generate_pokemon_table_html(pokemon_data):
    """
    Gera uma string HTML para uma tabela de Pokémon.
    """
    if pokemon_data.empty:
        return "<p>Nenhum Pokémon encontrado ou dados vazios.</p>"

    # Início da tabela HTML
    html_table = """
    <table class="pokemon-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Tipo 1</th>
                <th>Tipo 2</th>
                <th>HP</th>
                <th>Ataque</th>
                <th>Defesa</th>
                <th>Sp. Atk</th>
                <th>Sp. Def</th>
                <th>Velocidade</th>
                <th>Geração</th>
                <th>Lendário</th>
                <th>Altura</th>
                <th>Peso</th>
                <th>Exp. Base</th>
                <th>Sprite</th>
            </tr>
        </thead>
        <tbody>
    """

    # Adiciona cada linha de Pokémon
    for index, row in pokemon_data.iterrows():
        animated_sprite_url = ""
        try:
            # Tenta carregar a string da coluna 'sprites' usando ast.literal_eval
            # para lidar com strings que parecem dicionários Python (com aspas simples)
            sprites_dict = ast.literal_eval(row['sprites'])
            animated_sprite_url = sprites_dict.get('animated', '')
            # Se 'animated' não estiver disponível, tenta 'normal' como fallback
            if not animated_sprite_url:
                animated_sprite_url = sprites_dict.get('normal', '')
        except (ValueError, SyntaxError, AttributeError): # Captura erros de parsing do ast.literal_eval
            # Lida com casos onde a string não é um dicionário válido ou é NaN
            animated_sprite_url = "" # Deixa vazio se houver erro

        # --- LINHA ADICIONADA PARA DEBUG ---
        print(f"Pokémon: {row['Name']}, URL do Sprite: {animated_sprite_url}")
        # --- FIM DA LINHA ADICIONADA ---

        # URL de placeholder caso a imagem não carregue
        placeholder_image = "https://placehold.co/60x60/cccccc/000000?text=No+Img"

        html_table += f"""
            <tr>
                <td>{row['#']}</td>
                <td>{row['Name']}</td>
                <td>{row['Type 1']}</td>
                <td>{row['Type 2'] if pd.notna(row['Type 2']) else '-'}</td>
                <td>{row['HP']}</td>
                <td>{row['Attack']}</td>
                <td>{row['Defense']}</td>
                <td>{row['Sp. Atk']}</td>
                <td>{row['Sp. Def']}</td>
                <td>{row['Speed']}</td>
                <td>{row['Generation']}</td>
                <td>{'Sim' if row['Legendary'] else 'Não'}</td>
                <td>{row['height']}</td>
                <td>{row['weight']}</td>
                <td>{row['base_experience']}</td>
                <td>
                    <img src="{animated_sprite_url if animated_sprite_url else placeholder_image}"
                         alt="{row['Name']} Sprite"
                         class="pokemon-sprite"
                         onerror="this.onerror=null;this.src='{placeholder_image}';"
                    >
                </td>
            </tr>
        """
    # Fim da tabela HTML
    html_table += """
        </tbody>
    </table>
    """
    return html_table

# --- Script Principal ---
def main():
    try:
        # Carrega o dataset de Pokémon usando pandas
        # Certifique-se de que o arquivo final_pokemon.csv esteja na mesma pasta do script
        df_pokemon = pd.read_csv(POKEMON_CSV_FILE)

        # Seleciona as colunas que queremos exibir e limita o número de Pokémon
        # As colunas devem corresponder exatamente aos nomes no seu CSV
        df_display = df_pokemon.head(NUM_POKEMON_TO_SHOW)[[
            '#', 'Name', 'Type 1', 'Type 2', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary', 'height', 'weight', 'base_experience', 'sprites'
        ]]

        # Gera o HTML da tabela de Pokémon
        pokemon_table_html = generate_pokemon_table_html(df_display)

        # Data e hora da geração da página
        current_generation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Conteúdo HTML completo da página
        full_html_content = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokedex Simples - Dados Kaggle</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Pokedex</h1>
        {pokemon_table_html}
        <p class="info-footer">
            Dados gerados em: {current_generation_time}
        </p>
        <button onclick="location.reload()">Atualizar Pokedex</button>
    </div>
</body>
</html>
        """

        # Escreve o conteúdo HTML no arquivo
        with open(OUTPUT_HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(full_html_content)

        print(f"Pokedex HTML '{OUTPUT_HTML_FILE}' gerada/atualizada com sucesso.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{POKEMON_CSV_FILE}' não foi encontrado. Certifique-se de que ele está na mesma pasta do script.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
