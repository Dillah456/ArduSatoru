from flask import Flask, render_template, request
import json

app = Flask(__name__)

DATA_FILE = "data_wisata.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def expert_system(domisili=None, uang=None, waktu=None):
    data = load_data()
    hasil = []

    for wisata in data:
        cocok = True
        alasan = []

        # Rule Domisili
        if domisili:
            if wisata["domisili"].lower() == domisili.lower():
                alasan.append(f"sesuai dengan domisili Anda ({domisili})")
            else:
                cocok = False

        # Rule Biaya
        if uang:
            if wisata["uang_min"] <= uang <= wisata["uang_max"]:
                alasan.append(f"sesuai dengan anggaran Anda (Rp{uang})")
            else:
                cocok = False

        # Rule Waktu
        if waktu:
            if waktu >= wisata["waktu"]:
                alasan.append(f"dapat dikunjungi dalam waktu {waktu} hari")
            else:
                cocok = False

        if cocok:
            hasil.append({
                "nama": wisata["nama_tempat"],
                "alasan": alasan
            })

    return hasil


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
