from flask import Flask, render_template, request

app = Flask(__name__)

# Data gejala: kode -> (nama, bobot)  (Tabel 1 jurnal)
GEJALA = {
    "G01": ("Bulu rontok yang menyebabkan kebotakan", 3),
    "G02": ("Ada kerak berwarna putih di sekitar daun telinga", 5),
    "G03": ("Kulit terlihat bersisik", 5),
    "G04": ("Gatal sekitar telinga", 1),
    "G05": ("Sering menggoyangkan/menggelengkan kepala", 3),
    "G06": ("Sering menggaruk telinga hingga terdapat luka", 5),
    "G07": ("Muncul cairan berbau tidak sedap dari dalam telinga", 5),
    "G08": ("Posisi kepala miring dan tidak mampu berjalan lurus", 3),
    "G09": ("Mata belekan", 1),
    "G10": ("Perut buncit tapi badan kurus", 5),
    "G11": ("Diare", 3),
    "G12": ("Keluar cacing saat muntah atau pada kotoran", 5),
    "G13": ("Kerontokan bulu berbentuk lingkaran", 5),
    "G14": ("Sering menggaruk badan", 3),
    "G15": ("Agresif (sering menggigit dengan ganas)", 5),
    "G16": ("Sensitif (sering mencakar bila disentuh)", 5),
    "G17": ("Tidak nafsu makan", 1),
    "G18": ("Gelisah/suka bersembunyi/takut air", 3),
    "G19": ("Lemas/lesu", 1),
}

# Data penyakit dan gejalanya (Tabel 2 dan 3 jurnal)
PENYAKIT = {
    "Scabies": {
        "gejala": ["G01", "G02", "G03", "G04"],
        "deskripsi": "Penyakit kulit akibat tungau Notoedres cati; gatal dan keropeng di telinga, kaki, dan muka.",
    },
    "Otitis": {
        "gejala": ["G05", "G06", "G07", "G08", "G17", "G19"],
        "deskripsi": "Radang telinga (tungau, bakteri, jamur, alergi, dll.) pada telinga luar, tengah, atau dalam.",
    },
    "Cacingan": {
        "gejala": ["G09", "G10", "G11", "G12", "G17", "G19"],
        "deskripsi": "Infeksi endoparasit (cacing gelang/pita) yang menular lewat telur di kotoran atau air susu induk.",
    },
    "Ringworm": {
        "gejala": ["G01", "G13", "G14"],
        "deskripsi": "Infeksi jamur (mis. Microsporum canis) pada kulit dan bulu; rontok melingkar, kemerahan, gatal.",
    },
    "Rabies": {
        "gejala": ["G15", "G16", "G18", "G19"],
        "deskripsi": "Penyakit virus akut yang dapat menular ke manusia. Perlu penanganan dokter hewan segera.",
    },
}


def hitung_kemiripan(dipilih):
    """
    Kemiripan = Σ(similarity × bobot) / Σ bobot, dihitung pada gejala milik tiap kasus.
    Ketepatan = bobot gejala pilihan yang dimiliki kasus / total bobot gejala pilihan.
    """
    total_pilihan = sum(GEJALA[g][1] for g in dipilih)
    hasil = []

    for nama, data in PENYAKIT.items():
        gejala_kasus = data["gejala"]
        total_kasus = sum(GEJALA[g][1] for g in gejala_kasus)
        cocok = [g for g in gejala_kasus if g in dipilih]
        bobot_cocok = sum(GEJALA[g][1] for g in cocok)

        hasil.append({
            "nama": nama,
            "deskripsi": data["deskripsi"],
            "sim": bobot_cocok / total_kasus if total_kasus else 0,
            "pre": bobot_cocok / total_pilihan if total_pilihan else 0,
            "cocok": cocok,
            "belum": [g for g in gejala_kasus if g not in dipilih],
            "lain": [g for g in dipilih if g not in gejala_kasus],
        })

    hasil.sort(key=lambda r: (r["sim"], r["pre"]), reverse=True)
    return hasil


@app.template_filter("persen")
def persen(x):
    return f"{x * 100:.1f}".rstrip("0").rstrip(".") + "%"


@app.route("/", methods=["GET", "POST"])
def index():
    dipilih, hasil = [], None
    if request.method == "POST":
        # hanya terima kode gejala yang valid
        dipilih = [g for g in request.form.getlist("gejala") if g in GEJALA]
        if dipilih:
            hasil = hitung_kemiripan(dipilih)
    return render_template("index.html", gejala=GEJALA, dipilih=dipilih, hasil=hasil)


if __name__ == "__main__":
    app.run(debug=True)