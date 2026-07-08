from flask import Flask, render_template, request, session
import os
import random

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)

app.secret_key = "adivinhacao_secret_key_123_random_key"

@app.route("/", methods=["GET", "POST"])
def jogo():

    if "numero_secreto" not in session:
        session["numero_secreto"] = random.randint(1, 10)
        session["tentativas"] = 0

    mensagem = ""
    classe_mensagem = ""
    sucesso = False

    if request.method == "POST":
        action = request.form.get("action")

        if action == "reset":
            session["numero_secreto"] = random.randint(1, 10)
            session["tentativas"] = 0

        try:
            chute = int(request.form.get("chute", 0))
            session["tentativas"] += 1
            numero_secreto = session["numero_secreto"]

            if chute == numero_secreto:
                mensagem = f"Parabéns! Você acertou em {session['tentativas']} tentativa(s)."
                classe_mensagem = "Sucesso"
                sucesso = True

            elif chute < numero_secreto:
                mensagem = f"O número secreto é MAIOR que {chute}!"
                classe_mensagem = "alerta"

            else:
                mensagem = f"O número secreto é MENOR que {chute}!"
                classe_mensagem = "alerta"

        except ValueError:
            mensagem = "Por favor, insira um número inteiro válido."
            classe_mensagem = "erro"

    return render_template(
        "index.html",
        mensagem=mensagem,
        classe_mensagem=classe_mensagem,
        sucesso=sucesso,
        tentativas=session.get("tentativas", 0)
    )

if __name__ == "__main__":
    app.run(debug=True)