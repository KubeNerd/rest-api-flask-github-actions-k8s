import os, socket
from application import create_app


if os.getenv("FLASK_ENV") == "development":
    app = create_app("config.DevConfig")
else:
    app = create_app("config.ProdConfig")


host_address = socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    app.run(host=host_address, port=os.getenv("PORT", 5000), debug=False)
