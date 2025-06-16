from server.__main__ import app

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='127.0.0.1', use_reloader=True, ssl_context="adhoc")
