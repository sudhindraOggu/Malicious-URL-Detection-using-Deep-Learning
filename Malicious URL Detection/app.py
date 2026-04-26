from flask import Flask, request, render_template
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from feature_extractor import extract_features

app = Flask(__name__)

model = load_model("model.h5")
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        url = request.form["url"]

        features = extract_features(url)
        features = np.array(features).reshape(1, -1)
        features = scaler.transform(features)

        prediction = model.predict(features)[0][0]

        if prediction > 0.5:
            result = ("Legitimate Website", "green")
        else:
            result = ("Phishing Website", "red")

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)