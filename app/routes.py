from flask import Blueprint, render_template, jsonify, request
import requests

main_bp = Blueprint("main", __name__)

# Configurações das APIs
NOMINATIM_HEADERS = {
    "User-Agent": "solar-energy-predictor/1.0 (nicolas.jussiani@hotmail.com)"
}

PVGIS_PARAMS = {
    "peakpower": 1,
    "loss": 14,
    "angle": 35,
    "outputformat": "json"
}

OPENWEATHER_API_KEY = "cb8c650d1f8d8adbbbe2c4ea48113daf"  # Sua chave da API


@main_bp.route("/")
def index():
    return render_template("../index.html")


@main_bp.route("/get_solar", methods=["POST"])
def get_solar():
    try:
        lat = float(request.json.get("lat"))
        lon = float(request.json.get("lon"))

        response = requests.get(
            "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc",
            params={**PVGIS_PARAMS, "lat": lat, "lon": lon},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        annual_production = sum(month["E_m"] for month in data["outputs"]["monthly"])

        return jsonify({
            "annual_kwh": round(annual_production, 1),
            "efficiency": calculate_efficiency(annual_production)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/geocode", methods=["POST"])
def geocode():
    try:
        query = request.json.get("query")

        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 1},
            headers=NOMINATIM_HEADERS,
            timeout=5
        )
        response.raise_for_status()

        data = response.json()
        if not data:
            return jsonify({"error": "Local não encontrado"}), 404

        return jsonify({
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/get_weather", methods=["POST"])
def get_weather():
    try:
        lat = request.json.get("lat")
        lon = request.json.get("lon")

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt_br"

        response = requests.get(url)
        data = response.json()

        return jsonify({
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def calculate_efficiency(kwh):
    if kwh > 1600:
        return "Excelente"
    elif kwh > 1400:
        return "Boa"
    elif kwh > 1200:
        return "Média"
    return "Baixa"