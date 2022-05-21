import sys

from flask import Flask
import logging
from typing import Tuple

app = Flask(__name__)

app.config['DEBUG'] = True
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Jucker')


@app.route("/one")
def one() -> Tuple[str, int]:
    logger.info("Returned 201")
    return 'One more for the road', 201


@app.route("/two")
def two() -> Tuple[str, int]:
    logger.info("Returned 202")
    return 'Two beer or not two beer', 202


@app.route("/three")
def three() -> Tuple[str, int]:
    logger.info("Returned 203")
    return 'Ya three kings', 203


@app.route("/four")
def four() -> Tuple[str, int]:
    logger.info("Returned 204")
    return 'Four you', 204


@app.route("/five")
def five() -> Tuple[str, int]:
    logger.info("Returned 205")
    return 'Take five', 205


@app.route("/error")
def error_handler() -> Tuple[str, int]:
    a = 1 / 0
    logger.error("ZeroDivision")
    return "error", 500


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, threaded=True)
