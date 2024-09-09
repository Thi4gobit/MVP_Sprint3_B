import requests


def get_temperature(city_name, uf, date, time_hour):
    KEY = 'b4a3ccab'
    response = requests.get(f"https://api.hgbrasil.com/weather?key={KEY}&city_name={city_name},{uf}&date={date}&mode=all&fields=only_results,time,temp,forecast,max,min,date")
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Erro: {response.status_code}")
    
get_temperature('Rio de Janeiro', 'RJ', '2024-09-08', '12:00')