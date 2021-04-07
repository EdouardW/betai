from betai_flask import app

import json
from flask import make_response, Response

@app.route('/')
def version():
    response = make_response(json.dumps(
        {"app_name": "betai- Ligue 1 prediction"}))
    response.mimetype = 'application/json'
    return response