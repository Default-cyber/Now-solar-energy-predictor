document.getElementById('calc-form').addEventListener('submit', async e => {
  e.preventDefault();
  // Coleta valores
  const w = +document.getElementById('watt_per_panel').value;
  const n = +document.getElementById('num_panels').value;
  const h = +document.getElementById('sun_hours').value;
  const eff = +document.getElementById('efficiency').value / 100;
  const t = +document.getElementById('tariff').value;
  const cost = +document.getElementById('install_cost').value || 0;

  // Cálculo direto no cliente
  const daily = (w * h * eff) / 1000;                     // kWh/painel/dia :contentReference[oaicite:4]{index=4}
  const annual = daily * 365 * n;                         // kWh/ano :contentReference[oaicite:5]{index=5}
  const savings = annual * t;                             // R$/ano :contentReference[oaicite:6]{index=6}
  const payback = cost > 0 && savings>0 ? cost / savings : null;  // anos :contentReference[oaicite:7]{index=7}

  // Exibe resultados
  document.getElementById('res-annual-kwh').textContent = annual.toFixed(1);
  document.getElementById('res-savings').textContent    = savings.toFixed(2);
  if (payback) {
    document.getElementById('res-payback').textContent = `Payback aproximado: ${payback.toFixed(1)} anos`;
  }
  document.getElementById('calc-results').style.display = 'block';
});
