import pickle

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from flask import Flask, render_template, request, jsonify

model = pickle.load(open("finalized_model.sav", "rb"))

app = Flask(__name__)

print(model)


@app.route('/welcome')
def man():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def home():
    int_features = [x for x in request.form.values()]
    data_unseen = pd.DataFrame([int_features])
    pred = model.predict(data_unseen)

    return render_template('result.html', data=pred)


@app.route('/predict_api', methods=['POST'])
def predict_api():
    cols = [
        "duration",
        "src_bytes",
        "dst_bytes",
        "land",
        "wrong_fragment",
        "hot",
        "num_failed_logins",
        "logged_in",
        "num_compromised",
        "root_shell",
        "su_attempted",
        "num_root",
        "num_file_creations",
        "num_shells",
        "num_access_files",
        "num_outbound_cmds",
        "is_guest_login",
        "count",
        "srv_count",
        "serror_rate",
        "srv_serror_rate",
        "rerror_rate",
        "srv_rerror_rate",
        "same_srv_rate",
        "diff_srv_rate",
        "srv_diff_host_rate",
        "dst_host_count",
        "dst_host_srv_count",
        "dst_host_same_srv_rate",
        "dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate",
        "dst_host_serror_rate",
        "dst_host_srv_serror_rate",
        "dst_host_rerror_rate"
    ]
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data], cols)
    prediction = model.predict(data_unseen)
    predictvalue = prediction[0]
    if predictvalue == 0:
        prediction_class = 'Normal'
    else:
        prediction_class = 'Anamoly'

    return jsonify(prediction_class)


if __name__ == "__main__":
    app.run(debug=True, port=8084, use_reloader=False)
