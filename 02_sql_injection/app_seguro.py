import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
DB = Path(__file__).parent / "usuarios.db"

def seed():
    conn = sqlite3.connect(DB)
    conn.executescript(
        """
        DROP TABLE IF EXISTS usuarios;
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT,
            senha TEXT,
            saldo INTEGER
        );
        INSERT INTO usuarios (usuario, senha, saldo) VALUES
            ('ana', 'senha123', 1500),
            ('bruno', 'qwerty', 300),
            ('admin', 'S3nh@Admin', 99999);
        """
    )
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "")
    senha = request.form.get("senha", "")
    conn = sqlite3.connect(DB)
    query = "SELECT usuario, saldo FROM usuarios WHERE usuario = ? AND senha = ?"
    linha = conn.execute(query, (usuario, senha)).fetchone()
    conn.close()
    if linha:
        return render_template("painel.html", usuario=linha[0], saldo=linha[1])
    return render_template("login.html", erro="Usuario ou senha invalidos")

seed()

if __name__ == "__main__":
    app.run(port=5101, debug=True)
