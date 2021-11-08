from logging import debug
from app import zonaCipta_app

app = zonaCipta_app(True)

if __name__ == "__main__":
    app.run(debug=True)