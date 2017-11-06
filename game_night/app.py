from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    #from db import db
    #db.init_app(app)
    app.run(port=5000, debug=True)
