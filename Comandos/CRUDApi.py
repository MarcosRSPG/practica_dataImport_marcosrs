import requests

class ApiCRUD:
    def fetch_pokemon_data(pokemon_id):
        # Base URL for the Pokémon API
        url = f"https://pokeapi.co/api/v2/pokemon/"
        
        try:
            response = requests.get(url)
            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                # Extracting some information
                pokemon_info = {
                    "Name": data["name"],
                    "Types": [t["type"]["name"] for t in data["types"]]
                }
                return pokemon_info
            elif response.status_code == 404:
                return f"Pokémon '{pokemon_id}' not found."
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"