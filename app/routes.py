# Importações necessárias
from flask import Blueprint, render_template, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Configuração inicial
load_dotenv()

# Criação do Blueprint principal
main_bp = Blueprint("main", __name__)
CORS(main_bp)  # Habilita CORS para todas as rotas

# Configurações de API
API_CONFIG = {
    "nominatim": {
        "url": "https://nominatim.openstreetmap.org/search",
        "headers": {
            "User-Agent": os.getenv("NOMINATIM_USER_AGENT", "SolarApp/1.0 (contato@exemplo.com)")
        }
    },
    "pvgis": {
        "url": "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc",
        "params": {
            "peakpower": 1,
            "loss": 14,
            "angle": 35,
            "outputformat": "json"
        }
    },
    "openweather": {
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "api_key": os.getenv("OPENWEATHER_API_KEY")
    }
}


# Rota principal - Página inicial
@main_bp.route("/")
def index():
    """Renderiza a página principal"""
    return render_template("index.html")


# Rota de cálculo solar
@main_bp.route("/get_solar", methods=["POST"])
def get_solar():
    """Calcula dados de produção solar"""
    try:
        # Validação dos dados de entrada
        data = request.get_json()
        if not data or "lat" not in data or "lon" not in data:
            return jsonify({"error": "Coordenadas inválidas"}), 400

        lat = float(data["lat"])
        lon = float(data["lon"])

        # Chamada à API PVGIS
        response = requests.get(
            API_CONFIG["pvgis"]["url"],
            params={**API_CONFIG["pvgis"]["params"], "lat": lat, "lon": lon},
            timeout=15
        )
        response.raise_for_status()

        # Processamento dos dados
        pvgis_data = response.json()
        monthly_production = [month["E_m"] for month in pvgis_data["outputs"]["monthly"]]
        annual_production = sum(monthly_production)

        return jsonify({
            "annual_kwh": round(annual_production, 1),
            "monthly": monthly_production,
            "efficiency": calculate_efficiency(annual_production)
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout na API de energia solar"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro na API solar: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


# Rota de geocodificação
@main_bp.route("/geocode", methods=["POST"])
def geocode():
    """Converte endereço em coordenadas"""
    try:
        data = request.get_json()
        query = data.get("query")

        if not query or len(query) < 3:
            return jsonify({"error": "Consulta muito curta"}), 400

        # Chamada à API Nominatim
        response = requests.get(
            API_CONFIG["nominatim"]["url"],
            params={"q": query, "format": "json", "limit": 1},
            headers=API_CONFIG["nominatim"]["headers"],
            timeout=10
        )
        response.raise_for_status()

        # Processamento dos resultados
        results = response.json()
        if not results:
            return jsonify({"error": "Local não encontrado"}), 404

        return jsonify({
            "lat": float(results[0]["lat"]),
            "lon": float(results[0]["lon"]),
            "address": results[0]["display_name"]
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout na geocodificação"}), 504
    except Exception as e:
        return jsonify({"error": f"Erro de geocodificação: {str(e)}"}), 500


# Rota de dados climáticos
@main_bp.route("/get_weather", methods=["POST"])
def get_weather():
    """Obtém dados meteorológicos atuais"""
    try:
        # Verificação da API Key
        if not API_CONFIG["openweather"]["api_key"]:
            raise ValueError("Chave API não configurada")

        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")

        # Chamada à API OpenWeather
        response = requests.get(
            API_CONFIG["openweather"]["url"],
            params={
                "lat": lat,
                "lon": lon,
                "appid": API_CONFIG["openweather"]["api_key"],
                "units": "metric",
                "lang": "pt_br"
            },
            timeout=10
        )
        response.raise_for_status()

        # Processamento dos dados
        weather_data = response.json()
        return jsonify({
            "temp": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "description": weather_data["weather"][0]["description"].capitalize(),
            "wind_speed": weather_data["wind"]["speed"],
            "icon": weather_data["weather"][0]["icon"]
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout na API climática"}), 504
    except KeyError as e:
        return jsonify({"error": f"Dados climáticos incompletos: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Erro climático: {str(e)}"}), 500


# Função auxiliar - Cálculo de eficiência
def calculate_efficiency(kwh: float) -> str:
    """Classifica a eficiência com base na produção anual"""
    efficiency_map = [
        (2000, "Excelente"),
        (1600, "Muito Boa"),
        (1400, "Boa"),
        (1200, "Média"),
        (0, "Baixa")
    ]
    for threshold, category in efficiency_map:
        if kwh >= threshold:
            return category
    return "Desconhecida"