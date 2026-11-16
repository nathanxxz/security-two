import sqlite3
from pathlib import Path

import bcrypt
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DB = Path(__file__).parent / "usuarios_seguro.db"

def seed():
    conn = sqlite3.connect(DB)
    conn.executescript(
        """
        DROP TABLE IF EXISTS usuarios;
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT UNIQUE,
            senha TEXT
        );
        """
    )
    senha_hash = bcrypt.hashpw("maria2020".encode(), bcrypt.gensalt()).decode()
    conn.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("maria", senha_hash))
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    usuario = request.form.get("usuario", "")
    senha = request.form.get("senha", "")
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    conn = sqlite3.connect(DB)
    try:
        conn.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template("cadastro.html", erro="Usuario ja existe")
    conn.close()
    return redirect(url_for("admin"))

@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB)
    linhas = conn.execute("SELECT usuario, senha FROM usuarios").fetchall()
    conn.close()
    return render_template("admin.html", usuarios=linhas)

seed()

if __name__ == "__main__":
    app.run(port=5103, debug=True)
