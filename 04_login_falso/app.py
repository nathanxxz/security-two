from flask import Flask, render_template

app = Flask(__name__)

SINAIS = [
    "O endereco (URL) na barra do navegador nao era o site oficial; confira sempre o dominio.",
    "Nao havia HTTPS com cadeado valido.",
    "A pagina chegou por um link inesperado (e-mail ou mensagem) pedindo login.",
    "Havia pressa ou ameaca, como 'sua conta sera bloqueada', para tirar seu senso critico.",
    "O pedido de senha apareceu fora do contexto normal de uso.",
]

@app.route("/")
def index():
    return render_template("login_falso.html")

@app.route("/login", methods=["POST"])
def login():
    return render_template("revelacao.html", sinais=SINAIS)

if __name__ == "__main__":
    app.run(port=5005, debug=True)
