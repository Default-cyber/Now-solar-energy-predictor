<<<<<<< HEAD
// app/static/js/script.js

// Aguarda o DOM carregar antes de executar qualquer código
window.addEventListener("DOMContentLoaded", () => {
  // Inicializa o mapa
  const map = L.map('map').setView([-15.7942, -47.8822], 5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  let marker = null;
  const fetchOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    mode: 'cors',
    credentials: 'same-origin'
  };

  // Evento de clique no mapa
  map.on('click', async (e) => {
    try {
      await updatePosition(e.latlng.lat, e.latlng.lng);
    } catch (error) {
      showError(`Erro: ${error.message}`);
    }
  });

  // Busca por endereço
  const searchBtn = document.querySelector('.search-box button');
  if (searchBtn) {
    searchBtn.addEventListener('click', searchLocation);
  }

  async function searchLocation() {
    const query = document.getElementById('search-input').value.trim();
    if (!query) {
      showError("Digite um endereço válido!");
      return;
    }

    toggleLoading(searchBtn, true);
    try {
      const response = await fetch('/geocode', {
        ...fetchOptions,
        body: JSON.stringify({ query })
      });
      const data = await handleResponse(response);
      map.setView([data.lat, data.lon], 12);
      await updatePosition(data.lat, data.lon);
    } catch (error) {
      showError(`Falha na busca: ${error.message}`);
    } finally {
      toggleLoading(searchBtn, false);
    }
  }

  // Função principal de atualização
  async function updatePosition(lat, lon) {
    try {
      updateMarker(lat, lon);

      const [solarData, weatherData] = await Promise.all([
        fetchSolarData(lat, lon),
        fetchWeatherData(lat, lon)
      ]);

      updateSolarInfo(solarData);
      updateWeatherInfo(weatherData);
    } catch (error) {
      showError(`Atualização falhou: ${error.message}`);
    }
  }

  // Fetch dos dados solares
  async function fetchSolarData(lat, lon) {
    const response = await fetch('/get_solar', {
      ...fetchOptions,
      body: JSON.stringify({ lat, lon })
    });
    return handleResponse(response);
  }

  // Fetch dos dados climáticos
  async function fetchWeatherData(lat, lon) {
    const response = await fetch('/get_weather', {
      ...fetchOptions,
      body: JSON.stringify({ lat, lon })
    });
    return handleResponse(response);
  }

  // Tratamento padrão de resposta
  async function handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
    }
    return response.json();
  }

  // Atualiza o marcador no mapa
  function updateMarker(lat, lon) {
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lon], {
      icon: L.icon({
        iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
        iconSize: [25, 41]
      })
    }).addTo(map);
    const coordEl = document.getElementById('coordinates');
    if (coordEl) {
      coordEl.textContent = `Coordenadas: ${lat.toFixed(4)}, ${lon.toFixed(4)}`;
    }
  }

  // Atualiza as informações solares
  function updateSolarInfo(data) {
    const annualEl = document.getElementById('annual-production');
    const effEl = document.getElementById('efficiency');
    if (annualEl && effEl && data) {
      annualEl.textContent = `Produção Anual Estimada: ${data.annual_kwh} kWh/kWp`;
      effEl.textContent = data.efficiency;
      effEl.className = `efficiency-badge efficiency-${data.efficiency.toLowerCase()}`;
    }
  }

  // Atualiza as informações climáticas
  function updateWeatherInfo(data) {
    try {
      const tempEl = document.getElementById('weather-temp');
      const humEl = document.getElementById('weather-humidity');
      const windEl = document.getElementById('weather-wind');
      const descEl = document.getElementById('weather-description');
      const iconEl = document.getElementById('weather-icon');

      if (tempEl) tempEl.textContent = `${data.temp} °C`;
      if (humEl) humEl.textContent = `${data.humidity}%`;
      if (windEl) windEl.textContent = `${data.wind_speed} m/s`;
      if (descEl) descEl.textContent = data.description;
      if (iconEl) iconEl.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    } catch (err) {
      console.warn('Erro ao atualizar clima:', err);
    }
  }

  // Mostra ou esconde o botão de carregamento
  function toggleLoading(button, isLoading) {
    if (!button) return;
    button.disabled = isLoading;
    button.innerHTML = isLoading ? 'Buscando... ⌛' : '🔍 Buscar';
  }

  // Exibe alert de erro
  function showError(message) {
    console.error(message);
    alert(message);
  }
});
=======
const map = L.map('map').setView([-15.7942, -47.8822], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let marker = null;
const fetchOptions = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    mode: 'cors',
    credentials: 'same-origin'
};

// Clique no mapa
map.on('click', async (e) => {
    try {
        await updatePosition(e.latlng.lat, e.latlng.lng);
    } catch (error) {
        showError(`Erro: ${error.message}`);
    }
});

// Busca por endereço
async function searchLocation() {
    const query = document.getElementById('search-input').value.trim();
    const button = document.querySelector('button');

    if (!query) {
        showError("Digite um endereço válido!");
        return;
    }

    toggleLoading(button, true);

    try {
        const response = await fetch('/geocode', {
            ...fetchOptions,
            body: JSON.stringify({ query })
        });

        const data = await handleResponse(response);

        map.setView([data.lat, data.lon], 12);
        await updatePosition(data.lat, data.lon);

    } catch (error) {
        showError(`Falha na busca: ${error.message}`);
    } finally {
        toggleLoading(button, false);
    }
}

// Atualiza dados na interface
async function updatePosition(lat, lon) {
    try {
        updateMarker(lat, lon);

        const [solarData, weatherData] = await Promise.all([
            fetchSolarData(lat, lon),
            fetchWeatherData(lat, lon)
        ]);

        updateSolarInfo(solarData);
        updateWeatherInfo(weatherData);

    } catch (error) {
        showError(`Atualização falhou: ${error.message}`);
    }
}

// Funções auxiliares
async function fetchSolarData(lat, lon) {
    const response = await fetch('/get_solar', {
        ...fetchOptions,
        body: JSON.stringify({ lat, lon })
    });
    return handleResponse(response);
}

async function fetchWeatherData(lat, lon) {
    const response = await fetch('/get_weather', {
        ...fetchOptions,
        body: JSON.stringify({ lat, lon })
    });
    return handleResponse(response);
}

async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
    }
    return response.json();
}

function updateMarker(lat, lon) {
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lon], {
        icon: L.icon({
            iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
            iconSize: [25, 41]
        })
    }).addTo(map);
    document.getElementById('coordinates').textContent =
        `Coordenadas: ${lat.toFixed(4)}, ${lon.toFixed(4)}`;
}

function updateSolarInfo(data) {
    document.getElementById('annual-production').textContent =
        `Produção Anual Estimada: ${data.annual_kwh} kWh/kWp`;

    const efficiencyElement = document.getElementById('efficiency');
    efficiencyElement.textContent = data.efficiency;
    efficiencyElement.className = `efficiency-badge efficiency-${data.efficiency.toLowerCase()}`;
}

function updateWeatherInfo(data) {
    document.getElementById('weather-temp').textContent = `${data.temp} °C`;
    document.getElementById('weather-humidity').textContent = `${data.humidity}%`;
    document.getElementById('weather-description').textContent = data.description;
    document.getElementById('weather-wind').textContent = `${data.wind_speed} m/s`;
    document.getElementById('weather-icon').src =
        `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
}

function toggleLoading(button, isLoading) {
    button.disabled = isLoading;
    button.innerHTML = isLoading ? 'Buscando... ⌛' : '🔍 Buscar';
}

function showError(message) {
    console.error(message);
    alert(message);
}
>>>>>>> 1b4b43b343abefa05bf9751eba7bc9afdb15814f
