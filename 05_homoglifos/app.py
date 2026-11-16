from flask import Flask, render_template

app = Flask(__name__)

def monta_pares():
    a_cir = "\u0430"
    o_cir = "\u043e"
    pares = [
        {
            "legitimo": "contafacil.com",
            "impostor": "cont" + a_cir + "f" + a_cir + "cil.com",
            "truque": "Dois 'a' do alfabeto cirilico (parecem 'a' latino) no lugar dos 'a' reais.",
        },
        {
            "legitimo": "lojasegura.com",
            "impostor": "l" + o_cir + "jasegura.com",
            "truque": "Um 'o' do alfabeto cirilico no lugar do 'o' latino.",
        },
        {
            "legitimo": "mercado.com",
            "impostor": "rnercado.com",
            "truque": "As letras 'r' e 'n' juntas (rn) imitam visualmente um 'm'.",
        },
    ]
    for p in pares:
        try:
            p["punycode"] = p["impostor"].encode("idna").decode()
        except Exception:
            p["punycode"] = "(nao representavel em Punycode)"
        p["suspeitos"] = [
            f"{ch} = U+{ord(ch):04X}" for ch in p["impostor"] if ord(ch) > 127
        ]
    return pares

@app.route("/")
def index():
    return render_template("homoglifos.html", pares=monta_pares())

if __name__ == "__main__":
    app.run(port=5007, debug=True)
