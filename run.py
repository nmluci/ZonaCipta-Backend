from app import zonaCipta_app

# app = zonaCipta_app(True)
app = zonaCipta_app(False)

if __name__ == "__main__":
    app.run(debug=True)