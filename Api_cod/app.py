from flask import Flask, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route("/clima/<cidade>", methods=["GET"])
def obter_clima(cidade):
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt-br"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        dados = response.json()

        if response.status_code != 200:
            return jsonify({"erro": dados.get("message", "Erro ao buscar dados")}), response.status_code

        resultado = {
            "cidade": dados["name"],
            "temperatura": dados["main"]["temp"],
            "sensacao_termica": dados["main"]["feels_like"],
            "umidade": dados["main"]["humidity"],
            "descricao": dados["weather"][0]["description"]
        }
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
