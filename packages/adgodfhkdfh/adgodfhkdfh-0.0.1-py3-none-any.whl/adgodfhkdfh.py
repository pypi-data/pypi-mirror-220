import requests

class PlayerDataChecker:
    def __init__(self, ip):
        self.ip = ip

    def fetch_and_check_player_data(self):
        try:
            response = requests.get(f"http://{self.ip}/players.json", timeout=3)
            if response.status_code == 200:
                data = response.json()
            else:
                data = []

            pc = len(data)

            def getIdentifiers2(ids):
                return {id.split(':')[0]: id.split(':')[1] for id in ids}

            for player in data:
                name = player['name']
                identifiers = getIdentifiers2(player['identifiers'])
                discord = identifiers.get('discord')
                steam = identifiers.get('steam')
                license = identifiers.get('license')
                license2 = identifiers.get('license2')
                if not self.player_exists_in_api(name, discord, steam, license, license2):
                    if self.add_player_to_api(name, discord, steam, license, license2):
                        print(f"Player '{name}' added to the API.")
                    else:
                        print(f"Failed to add player '{name}' to the API.")
                else:
                    print(f"Player '{name}' already exists in the API.")

            print("Player data check completed.")
        except requests.exceptions.Timeout:
            print("The request to fetch player data from the API timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch player data from the API: {str(e)}")

    def player_exists_in_api(self, name, discord, steam, license, license2):
        api_key = "QK9FU8dkqp3gjgLPm6RHvQ4b3MReA89M"
        headers = {
            'API-Key': api_key
        }
        response = requests.get(f"http://{self.ip}:5000/protected", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for player_data in data:
                if (player_data['name'] == name and 
                    player_data['discordid'] == discord and 
                    player_data['steamid'] == steam and 
                    player_data['license'] == license and 
                    player_data['license2'] == license2):
                    return True
        return False

    def add_player_to_api(self, name, discord, steam, license, license2):
        api_key = "FpWLBbj1xVaybdDcohiLYRPmHkQvdbpT" 
        headers = {
            'API-Key': api_key,
            'Content-Type': 'application/json'
        }
        data = {
            'name': name,
            'discordid': discord,
            'steamid': steam,
            'license': license,
            'license2': license2
        }
        response = requests.post(f"http://{self.ip}:5000/send-data", json=data, headers=headers)
        if response.status_code == 200:
            print(f"Player '{name}' added to the API.")
            return True
        else:
            print(f"Failed to add player '{name}' to the API.")
            return False
        
