from blog import app


@app.route("/")
def home():
    return "Hellow Word"
