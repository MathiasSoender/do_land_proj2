import sys
sys.path.append("app")
from app import create_app, HOST, BASE_PORT


app = create_app()


if __name__ == "__main__":
    app.run(host=HOST, port=BASE_PORT, debug=True)
