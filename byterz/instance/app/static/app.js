// app/static/app.js - small UI enhancements
document.addEventListener("DOMContentLoaded", () => {
  const convButton = document.getElementById("convert");
  if (convButton) {
    convButton.addEventListener("click", async (e) => {
      e.preventDefault();
      const v = parseFloat(document.getElementById("w").value || 0);
      const unit = document.getElementById("unit").value || "kg";
      try {
        const r = await fetch(`/api/convert/weight?value=${v}&unit=${unit}`);
        const j = await r.json();
        document.getElementById("conv_out").textContent = `Earth: ${j.earth} ${j.unit} → Mars: ${j.mars} ${j.unit}`;
      } catch (err) {
        document.getElementById("conv_out").textContent = "Conversion failed";
      }
    });
  }
});