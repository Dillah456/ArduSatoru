from flask import Flask, render_template, request
import json

app = Flask(__name__)

DATA_FILE = "data_wisata.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def expert_system(domisili=None, uang=None, waktu=None):
    data = load_data()
    rekomendasi = []

    for wisata in data:
        cocok = True

        # Rule Domisili
        if domisili:
            if wisata["domisili"].lower() != domisili.lower():
                cocok = False

        # Rule Uang
        if uang:
            if not (wisata["uang_min"] <= uang <= wisata["uang_max"]):
                cocok = False

        # Rule Waktu
        if waktu:
            if waktu < wisata["waktu"]:
                cocok = False

        if cocok:
            rekomendasi.append(wisata["nama_tempat"])

    return rekomendasi


@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None

    if request.method == "POST":
        domisili = request.form.get("domisili")
        uang = request.form.get("uang")
        waktu = request.form.get("waktu")

        # Konversi jika diisi
        uang = int(uang) if uang else None
        waktu = int(waktu) if waktu else None

        hasil = expert_system(domisili, uang, waktu)

    return render_template("index.html", hasil=hasil)


if __name__ == "__main__":
    app.run(debug=True)
