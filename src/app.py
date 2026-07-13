from flask import Flask, render_template_string
import socket
import os
import sys
from datetime import datetime

app = Flask(__name__)

_request_count = 0
_start_time = datetime.now()


def get_container_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()


HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>☸️ Kubernetes Python Demo</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  @keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  body {
    min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #fff;
    background: linear-gradient(125deg, #6a11cb 0%, #2575fc 35%, #8e2de2 70%, #4a00e0 100%);
    background-size: 300% 300%;
    animation: gradientShift 15s ease infinite;
    padding: 40px 20px;
    overflow-x: hidden;
  }

  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15), transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(255,0,200,0.18), transparent 50%);
    pointer-events: none;
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
  }

  .header {
    text-align: center;
    margin-bottom: 50px;
    animation: fadeUp 0.8s ease-out;
  }

  .logo {
    font-size: 80px;
    display: inline-block;
    animation: float 4s ease-in-out infinite;
    filter: drop-shadow(0 4px 20px rgba(0,0,0,0.3));
  }

  .header h1 {
    font-size: 3.2rem;
    font-weight: 800;
    margin: 10px 0;
    background: linear-gradient(90deg, #fff, #e0d4ff, #fff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }

  .header .subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    font-weight: 300;
    margin-top: 8px;
  }

  .header .pod-name {
    display: inline-block;
    margin-top: 16px;
    padding: 8px 20px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 100px;
    font-family: "SF Mono", Monaco, Consolas, monospace;
    font-size: 0.95rem;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
  }

  .card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
    animation: fadeUp 0.8s ease-out backwards;
  }

  .card:nth-child(1) { animation-delay: 0.1s; }
  .card:nth-child(2) { animation-delay: 0.2s; }
  .card:nth-child(3) { animation-delay: 0.3s; }
  .card:nth-child(4) { animation-delay: 0.4s; }
  .card:nth-child(5) { animation-delay: 0.5s; }
  .card:nth-child(6) { animation-delay: 0.6s; }

  .card:hover {
    transform: translateY(-6px) scale(1.02);
    background: rgba(255, 255, 255, 0.18);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .card .icon {
    font-size: 32px;
    margin-bottom: 10px;
    display: block;
  }

  .card .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    opacity: 0.75;
    margin-bottom: 6px;
    font-weight: 600;
  }

  .card .value {
    font-size: 1.15rem;
    font-weight: 700;
    word-break: break-all;
    font-family: "SF Mono", Monaco, Consolas, monospace;
  }

  .card .value.small { font-size: 0.95rem; }

  .badge {
    display: inline-block;
    margin-top: 6px;
    padding: 2px 10px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 500;
  }

  .badge.warn { background: rgba(255, 200, 0, 0.25); }
  .badge.ok   { background: rgba(0, 220, 130, 0.25); }

  .footer {
    text-align: center;
    padding: 24px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    font-size: 0.9rem;
    opacity: 0.9;
    animation: fadeUp 0.8s ease-out 0.7s backwards;
  }

  .footer .dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #00ff88;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 10px #00ff88;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.4; }
  }

  @media (max-width: 600px) {
    .header h1 { font-size: 2rem; }
    .logo { font-size: 60px; }
  }
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="logo">☸️</span>
      <h1>Kubernetes Python Demo</h1>
      <p class="subtitle">Hola desde un Pod corriendo en tu cluster</p>
      <div class="pod-name">📦 {{ hostname }}</div>
    </div>

    <div class="grid">
      <div class="card">
        <span class="icon">🌐</span>
        <div class="label">Server IP</div>
        <div class="value">{{ container_ip }}</div>
        <span class="badge ok">container</span>
      </div>

      <div class="card">
        <span class="icon">🛰️</span>
        <div class="label">Pod IP</div>
        <div class="value small">{{ pod_ip }}</div>
        {% if pod_ip_available %}
          <span class="badge ok">k8s</span>
        {% else %}
          <span class="badge warn">downward API</span>
        {% endif %}
      </div>

      <div class="card">
        <span class="icon">🗂️</span>
        <div class="label">Namespace</div>
        <div class="value">{{ namespace }}</div>
        {% if namespace_available %}
          <span class="badge ok">k8s</span>
        {% else %}
          <span class="badge warn">N/D</span>
        {% endif %}
      </div>

      <div class="card">
        <span class="icon">🖥️</span>
        <div class="label">Node</div>
        <div class="value small">{{ node_name }}</div>
        {% if node_available %}
          <span class="badge ok">k8s</span>
        {% else %}
          <span class="badge warn">N/D</span>
        {% endif %}
      </div>

      <div class="card">
        <span class="icon">📊</span>
        <div class="label">Requests en este Pod</div>
        <div class="value">{{ request_count }}</div>
        <span class="badge ok">live</span>
      </div>

      <div class="card">
        <span class="icon">⏱️</span>
        <div class="label">Uptime del Pod</div>
        <div class="value small">{{ uptime }}</div>
        <span class="badge ok">live</span>
      </div>
    </div>

    <div class="footer">
      <span class="dot"></span>
      Served by Flask {{ flask_version }} · Python {{ python_version }} · {{ timestamp }}
    </div>
  </div>
</body>
</html>
"""


def _humanize_uptime(delta) -> str:
    secs = int(delta.total_seconds())
    days, secs = divmod(secs, 86400)
    hours, secs = divmod(secs, 3600)
    minutes, seconds = divmod(secs, 60)
    parts = []
    if days:    parts.append(f"{days}d")
    if hours:   parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


@app.route("/")
def hello():
    global _request_count
    _request_count += 1

    hostname = os.environ.get("HOSTNAME") or socket.gethostname()
    pod_ip = os.environ.get("POD_IP", "N/D")
    namespace = os.environ.get("POD_NAMESPACE", "N/D")
    node_name = os.environ.get("NODE_NAME", "N/D")

    return render_template_string(
        HTML,
        hostname=hostname,
        container_ip=get_container_ip(),
        pod_ip=pod_ip,
        pod_ip_available=pod_ip != "N/D",
        namespace=namespace,
        namespace_available=namespace != "N/D",
        node_name=node_name,
        node_available=node_name != "N/D",
        request_count=_request_count,
        uptime=_humanize_uptime(datetime.now() - _start_time),
        flask_version=__import__("flask").__version__,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
