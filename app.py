from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def resume():
    title = "My Resume"
    return render_template('resume.html', title=title)

if __name__ == "__main__":
    app.run(debug=True)

