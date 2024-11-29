import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), "app/templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "app/static"))
app.secret_key = 'secret-key-sdsfs'  # Замініть на унікальний ключ

# Жорстко задані дані для автентифікації
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username
            flash("Успішний вхід!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Невірний логін або пароль", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        flash("Будь ласка, увійдіть!", "warning")
        return redirect(url_for("login"))

    user = session["user"]
    cookies = request.cookies.items()

    if request.method == "POST":
        if "add_cookie" in request.form:
            key = request.form.get("cookie_key")
            value = request.form.get("cookie_value")
            resp = make_response(redirect(url_for("profile")))
            resp.set_cookie(key, value, max_age=3600)
            flash(f"Кукі '{key}' додано.", "success")
            return resp
        elif "delete_cookie" in request.form:
            key = request.form.get("cookie_key")
            resp = make_response(redirect(url_for("profile")))
            if key:
                resp.delete_cookie(key)
                flash(f"Кукі '{key}' видалено.", "info")
            else:
                for key, _ in cookies:
                    resp.delete_cookie(key)
                flash("Усі кукі видалено.", "info")
            return resp

    return render_template("profile.html", user=user, cookies=cookies)


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for("login"))


@app.route("/change-theme/<theme>")
def change_theme(theme):
    if theme in ["light", "dark"]:
        session["theme"] = theme
        flash(f"Тема змінена на {theme}.", "success")
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)
