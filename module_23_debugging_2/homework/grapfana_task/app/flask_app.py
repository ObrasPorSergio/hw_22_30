import time
import random

from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/connection")
@metrics.counter(
    "counter_collection", "Number of invocations per connection.", labels={
        "status": lambda resp: resp.status_code
    })
def first_route():
    time.sleep(random.random() * 0.2)
    if random.randint(1, 10) % 2 == 0:
        return "ok"
    else:
        return "error", 400


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
