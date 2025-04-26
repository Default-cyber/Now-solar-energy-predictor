<<<<<<< HEAD
import os
from dotenv import load_dotenv
from flask import Blueprint, render_template, jsonify, request, session
from flask_cors import CORS
import requests

# Carrega .env
load_dotenv()

main_bp = Blueprint("main", __name__)
CORS(main_bp)

# Configurações de APIs externas
API_CONFIG = {
    "nominatim": {
        "url": "https://nominatim.openstreetmap.org/search",
        "headers": {"User-Agent": os.getenv("NOMINATIM_USER_AGENT", "SolarApp/1.0")}
    },
    "pvgis": {
        "url": "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc",
        "params": {"peakpower": 1, "loss": 14, "angle": 35, "outputformat": "json"}
=======
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
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
    },
    "openweather": {
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "api_key": os.getenv("OPENWEATHER_API_KEY")
    }
}


<<<<<<< HEAD
@main_bp.route("/")
def home_page():
    """Tela inicial: escolha entre simulador ou calculadora."""
    theme = session.get("theme", "light")
    return render_template("home.html", theme=theme)


@main_bp.route("/map")
def map_page():
    """Simulador de energia solar com mapa."""
    theme = session.get("theme", "light")
    return render_template("index.html", theme=theme)


@main_bp.route("/calculator")
def calculator_page():
    """Calculadora de geração e economia de energia."""
    theme = session.get("theme", "light")
    return render_template("calculator.html", theme=theme)


@main_bp.route("/get_solar", methods=["POST"])
def get_solar():
    """Chama PVGIS para cálculo de produção solar."""
    try:
        data = request.get_json() or {}
        lat = float(data.get("lat", 0))
        lon = float(data.get("lon", 0))
        if not lat or not lon:
            return jsonify({"error": "Coordenadas inválidas"}), 400

        resp = requests.get(
=======
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
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
            API_CONFIG["pvgis"]["url"],
            params={**API_CONFIG["pvgis"]["params"], "lat": lat, "lon": lon},
            timeout=15
        )
<<<<<<< HEAD
        resp.raise_for_status()
        pvgis = resp.json()

        monthly = [m["E_m"] for m in pvgis["outputs"]["monthly"]]
        annual = sum(monthly)

        return jsonify({
            "annual_kwh": round(annual, 1),
            "monthly": monthly,
            "efficiency": calculate_efficiency(annual)
        })
    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout na API PVGIS"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/geocode", methods=["POST"])
def geocode():
    """Converte endereço em coordenadas via Nominatim."""
    try:
        data = request.get_json() or {}
        q = data.get("query", "")
        if len(q) < 3:
            return jsonify({"error": "Consulta muito curta"}), 400

        resp = requests.get(
            API_CONFIG["nominatim"]["url"],
            params={"q": q, "format": "json", "limit": 1},
            headers=API_CONFIG["nominatim"]["headers"],
            timeout=10
        )
        resp.raise_for_status()
        res = resp.json()
        if not res:
            return jsonify({"error": "Local não encontrado"}), 404

        return jsonify({
            "lat": float(res[0]["lat"]),
            "lon": float(res[0]["lon"]),
            "address": res[0]["display_name"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/get_weather", methods=["POST"])
def get_weather():
    """Obtém condições climáticas do OpenWeather."""
    try:
        key = API_CONFIG["openweather"]["api_key"]
        if not key:
            return jsonify({"error": "Chave API não configurada"}), 500

        data = request.get_json() or {}
        lat = data.get("lat")
        lon = data.get("lon")

        resp = requests.get(
            API_CONFIG["openweather"]["url"],
            params={"lat": lat, "lon": lon, "appid": key, "units": "metric", "lang": "pt_br"},
            timeout=10
        )
        resp.raise_for_status()
        w = resp.json()

        return jsonify({
            "temp": w["main"]["temp"],
            "humidity": w["main"]["humidity"],
            "description": w["weather"][0]["description"].capitalize(),
            "wind_speed": w["wind"]["speed"],
            "icon": w["weather"][0]["icon"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_bp.route("/calculate", methods=["POST"])
def calculate():
    """Calcula geração anual e economia financeira."""
    try:
        d = request.get_json() or {}
        w    = float(d.get("watt_per_panel", 0))
        n    = int(d.get("num_panels", 0))
        h    = float(d.get("sun_hours", 0))
        eff  = float(d.get("efficiency", 0)) / 100
        t    = float(d.get("tariff", 0))
        cost = float(d.get("install_cost", 0))

        daily   = w * h * eff / 1000
        annual  = daily * 365 * n
        savings = annual * t
        payback = (cost / savings) if cost and savings else None

        return jsonify({
            "annual_kwh": round(annual, 1),
            "savings":    round(savings, 2),
            "payback":    round(payback, 1) if payback else None
        })
    except Exception as e:
        return jsonify({"error": f"Erro no cálculo: {e}"}), 400


def calculate_efficiency(kwh: float) -> str:
    """Classifica a eficiência com base na produção anual."""
    for thresh, cat in [
=======
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
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
        (2000, "Excelente"),
        (1600, "Muito Boa"),
        (1400, "Boa"),
        (1200, "Média"),
<<<<<<< HEAD
        (0,    "Baixa"),
    ]:
        if kwh >= thresh:
            return cat
    return "Desconhecida"
=======
        (0, "Baixa")
    ]
    for threshold, category in efficiency_map:
        if kwh >= threshold:
            return category
    return "Desconhecida"
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
