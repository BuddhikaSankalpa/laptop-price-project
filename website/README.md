Laptop Price Predictor — front-end + minimal backend

Files created
- index.html — single-page front-end with a form to enter laptop specs
- static/styles.css — basic responsive styles
- static/predict.js — client-side JS that POSTs JSON to /predict and shows the result (with a client-side fallback)
- app.py — minimal Flask app that serves the page and exposes /predict; will attempt to use model/predictor.pickle if present
- requirements.txt — lists Flask

Quick start (PowerShell)
1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

(If PowerShell blocks script execution, run once as Admin: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)

2. Install dependencies and run the backend:

```powershell
pip install -r requirements.txt
python app.py
```

3. Open http://127.0.0.1:5000/ in your browser and test the form.

Notes
- If `model/predictor.pickle` exists (one level up in the `model` folder) and is a pickled object with a `predict` method that accepts the feature vector used in `app.py`, the Flask app will try to use it. Otherwise the app returns a simple heuristic-based price.
- If you only want to serve the static page without the backend, you can open `index.html` directly or run `python -m http.server` and open the page; however the `/predict` fetch will fail unless you run a backend.

If you want, I can now:
- Wire the form fields to match the exact features your pickled model expects (tell me the feature order), or
- Add more UI polish, validation, and example presets.
