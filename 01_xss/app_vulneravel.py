from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
recados = []

@app.route("/")
def index():
    return render_template("mural_vulneravel.html", recados=recados)

@app.route("/recado", methods=["POST"])
def recado():
    recados.append(request.form.get("texto", ""))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=5002, debug=True)
