from app import create_app
import os, sys

print("🔥 RUN.PY EXECUTED 🔥")
print("FILE:", os.path.abspath(__file__))
print("PYTHON:", sys.executable)

app = create_app()

@app.route("/ping",methods=["GET"])
def ping():
    return "PING OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
