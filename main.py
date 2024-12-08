from flask import Flask, render_template_string, request
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

registry = CollectorRegistry()


# Alap metrikák hozzáadása (CPU, memória stb.)
def collect_default_metrics():
    from prometheus_client import Summary, Gauge

    request_latency = Summary('http_request_latency_seconds', 'Request latency', ['method', 'endpoint'])
    request_in_progress = Gauge('http_requests_in_progress', 'Requests in progress', ['method', 'endpoint'])

    return [request_latency, request_in_progress]


default_metrics = collect_default_metrics()
for metric in default_metrics:
    registry.register(metric)

# HTTP kérés időtartam
http_request_duration = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'path', 'status_code'],
    registry=registry,
    buckets=[0.01, 0.05, 0.1, 0.5, 1]
)

# HTTP kérések száma összesen
http_request_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'path', 'status_code'],
    registry=registry
)

# /current_time végpont hívási száma
current_time_requests = Counter(
    'current_time_requests_total',
    'Total number of /current_time requests',
    registry=registry
)

# /fun_fact végpont hívási száma
fun_fact_requests = Counter(
    'fun_fact_requests_total',
    'Total number of /fun_fact requests',
    registry=registry
)


# Biztonsági fejlécek beállítása
@app.after_request
def set_security_headers(response):
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


# Alap végpont
@app.route('/')
def home():
    return render_template_string('''
        <h1>Elérhető aloldalak</h1>
        <ul>
            <li><a href="/current_time">localhost:5000/current_time</a></li>
            <li><a href="/fun_fact">localhost:5000/fun_fact</a></li>
            <li><a href="/metrics">localhost:5000/metrics</a></li>
        </ul>
    ''')


# Végpont az aktuális idő lekérdezéséhez
@app.route('/current_time', methods=['GET'])
def current_time():
    start_time = time.time()
    response = time.strftime('%Y-%m-%d %H:%M:%S')
    elapsed_time = time.time() - start_time
    http_request_duration.labels(method='GET', path='/current_time', status_code='200').observe(elapsed_time)
    http_request_total.labels(method='GET', path='/current_time', status_code='200').inc()
    current_time_requests.inc()
    return response


# Végpont fun-fact lekérdezéséhez
@app.route('/fun_fact', methods=['GET'])
def fun_fact():
    start_time = time.time()
    fun_fact = "A banán bogyós gyümölcs, míg az eper nem."
    response = fun_fact
    elapsed_time = time.time() - start_time
    http_request_duration.labels(method='GET', path='/fun_fact', status_code='200').observe(elapsed_time)
    http_request_total.labels(method='GET', path='/fun_fact', status_code='200').inc()
    fun_fact_requests.inc()
    return response


# Végpont metrikák lekérdezéséhez
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
