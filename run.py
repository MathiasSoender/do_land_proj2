import sys
sys.path.append("app")
from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)