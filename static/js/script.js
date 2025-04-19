const map = L.map('map').setView([-15.7942, -47.8822], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let marker = null;

// Clique no mapa
map.on('click', async (e) => {
    updatePosition(e.latlng.lat, e.latlng.lng);
});

async function searchLocation() {
    const query = document.getElementById('search-input').value.trim();
    const button = document.querySelector('button');

    if (!query) {
        alert("Digite um endereço válido!");
        return;
    }

    button.disabled = true;
    button.innerHTML = 'Buscando... ⌛';

    try {
        const response = await fetch('/geocode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
        const data = await response.json();
        if (data.error) throw new Error(data.error);

        map.setView([data.lat, data.lon], 12);
        await updatePosition(data.lat, data.lon);

    } catch (error) {
        console.error('Erro na busca:', error);
        alert(`Erro: ${error.message}`);
    } finally {
        button.disabled = false;
        button.innerHTML = '🔍 Buscar';
    }
}

async function updatePosition(lat, lon) {
    try {
        // Limpa marcador antigo
        if (marker) map.removeLayer(marker);

        // Novo marcador
        marker = L.marker([lat, lon], {
            icon: L.icon({
                iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
                iconSize: [25, 41]
            })
        }).addTo(map);

        // Atualiza coordenadas
        document.getElementById('coordinates').textContent = `Coordenadas: ${lat.toFixed(4)}, ${lon.toFixed(4)}`;

        // Busca dados SOLARES e CLIMÁTICOS simultaneamente
        const [solarRes, weatherRes] = await Promise.all([
            fetch('/get_solar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lon })
            }),
            fetch('/get_weather', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lon })
            })
        ]);

        // Processa dados solares
        if (!solarRes.ok) throw new Error('Erro nos dados solares');
        const solarData = await solarRes.json();

        document.getElementById('annual-production').textContent =
            `Produção Anual Estimada: ${solarData.annual_kwh} kWh/kWp`;

        const efficiencyElement = document.getElementById('efficiency');
        efficiencyElement.textContent = solarData.efficiency;
        efficiencyElement.className = `efficiency-badge efficiency-${solarData.efficiency.toLowerCase()}`;

        // Processa dados climáticos
        if (!weatherRes.ok) throw new Error('Erro nos dados climáticos');
        const weatherData = await weatherRes.json();

        document.getElementById('weather-temp').textContent = `${weatherData.temp} °C`;
        document.getElementById('weather-humidity').textContent = `${weatherData.humidity}%`;
        document.getElementById('weather-description').textContent = weatherData.description;
        document.getElementById('weather-wind').textContent = `${weatherData.wind_speed} m/s`;
        document.getElementById('weather-icon').src =
            `https://openweathermap.org/img/wn/${weatherData.icon}@2x.png`;

    } catch (error) {
        console.error('Erro ao atualizar posição:', error);
        alert(`Erro: ${error.message}`);
    }
}