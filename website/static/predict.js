document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('predict-form');
  const resultEl = document.getElementById('result');

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(form);
    const payload = {
      brand: fd.get('brand') || null,
      year: Number(fd.get('year')) || 2022,
      ram: Number(fd.get('ram')) || 0,
      storage: Number(fd.get('storage')) || 0,
      ssd: Number(fd.get('ssd')) === 1,
      cpu: fd.get('cpu') || null
    };

    resultEl.innerHTML = '<em>Requesting prediction…</em>';

    try{
      const resp = await fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      });

      if(!resp.ok) throw new Error('Non-OK HTTP status: '+resp.status);
      const data = await resp.json();
      if(data && typeof data.price !== 'undefined'){
        resultEl.innerHTML = `<strong>Predicted price:</strong> LKR ${Number(data.price).toFixed(2)} <small>(${data.source||'unknown'})</small>`;
      } else {
        resultEl.innerHTML = '<span style="color:#b91c1c">Unexpected response from server.</span>';
      }
    }catch(err){
      console.warn('Fetch failed, showing local heuristic fallback:', err);
      // heuristic fallback in the browser
      const base = 200;
      const age = Math.max(0, 2025 - (payload.year || 2022));
  const eurPrice = Math.max(10, base + payload.ram*20 + payload.storage*0.3 - age*25 + (payload.ssd?50:0));
  const lkrPrice = eurPrice * 355; // convert EUR -> LKR
  resultEl.innerHTML = `<strong>Predicted price (fallback):</strong> LKR ${lkrPrice.toFixed(2)} <small>(client-side heuristic)</small>`;
    }
  });
});