// theme-toggle.js

document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("theme-toggle");
  const htmlEl   = document.documentElement;

  // 1) Carrega tema salvo em localStorage
  const saved = localStorage.getItem("theme");
  if (saved === "dark") htmlEl.classList.add("dark-mode");

  // 2) Aplica reduce-motion se preferido pelo usuário
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    htmlEl.classList.add("reduce-motion");
  }

  // 3) Alterna tema ao clicar
  toggleBtn.addEventListener("click", () => {
    htmlEl.classList.toggle("dark-mode");
    const theme = htmlEl.classList.contains("dark-mode") ? "dark" : "light";
    localStorage.setItem("theme", theme);

    // 4) Notifica o servidor (opcional)
    fetch("/set-theme", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ theme })
    });
  });
});
