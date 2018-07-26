from flask import Flask

# Name of file tells Flask where templates, static files, etc are
app = Flask(__name__)

# Need to import routes here to avoid circular import
from webapp import routes