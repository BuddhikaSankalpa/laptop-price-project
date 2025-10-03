from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# setup application
app = Flask(__name__)

MODEL_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'predictor.pickle'))


def load_model():
    if os.path.exists(MODEL_FILE):
        try:
            with open(MODEL_FILE, 'rb') as file:
                return pickle.load(file)
        except Exception:
            return None
    return None

MODEL = load_model()


def prediction(lst):
    # if a pickled model is available, use it; otherwise raise
    if MODEL is None:
        raise FileNotFoundError('Model file not found')
    pred_value = MODEL.predict([lst])
    return pred_value


@app.route('/', methods=['POST', 'GET'])
def index():
    pred_value = None
    error = None
    if request.method == 'POST':
        try:
            ram = request.form.get('ram', type=int)
            weight = request.form.get('weight', type=float)
            company = request.form.get('company')
            typename = request.form.get('typename')
            opsys = request.form.get('opsys')
            cpu = request.form.get('cpuname')
            gpu = request.form.get('gpuname')
            touchscreen = request.form.getlist('touchscreen')
            ips = request.form.getlist('ips')

            feature_list = []

            feature_list.append(int(ram or 0))
            feature_list.append(float(weight or 0.0))
            feature_list.append(len(touchscreen))
            feature_list.append(len(ips))

            company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
            typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
            opsys_list = ['linux','mac','other','windows']
            cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
            gpu_list = ['amd','intel','nvidia']

            def traverse_list(lst, value):
                for item in lst:
                    if item == value:
                        feature_list.append(1)
                    else:
                        feature_list.append(0)

            traverse_list(company_list, company)
            traverse_list(typename_list, typename)
            traverse_list(opsys_list, opsys)
            traverse_list(cpu_list, cpu)
            traverse_list(gpu_list, gpu)

            # Predict using model if available, otherwise compute heuristic
            try:
                pred_raw = prediction(feature_list)
                # model returns price in EUR; convert to LKR using 1 EUR = 355 LKR
                pred_value = np.round(pred_raw[0], 2) * 355
            except FileNotFoundError:
                # heuristic fallback
                base = 200.0
                age = max(0, 2025 - (int(request.form.get('year', 2022))))
                ram_val = int(ram or 0)
                storage_val = int(request.form.get('storage', 0))
                # heuristic result in EUR -> convert to LKR
                eur_price = round(max(5.0, base + ram_val * 20.0 + storage_val * 0.3 - age * 25.0 + (50.0 if len(touchscreen) else 0.0)), 2)
                pred_value = round(eur_price * 355, 2)

        except Exception as e:
            error = str(e)

    return render_template('index.html', pred_value=pred_value, error=error)


if __name__ == '__main__':
    app.run(debug=True)
