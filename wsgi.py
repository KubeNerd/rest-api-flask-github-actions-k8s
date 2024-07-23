import os
from application import create_app

if os.getenv('FLASK_ENV') == "development":
    app = create_app('config.DevConfig')
else:
    app = create_app('config.ProdConfig')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000), debug=True)
