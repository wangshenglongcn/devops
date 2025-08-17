import queue, threading
from collections import Counter, defaultdict

EVENTS = queue.SimpleQueue()
REQUEST_COUNT = Counter()  # (method, path, status) -> count
REQUEST_TOTAL_COUONT = defaultdict(int)  # (method, path) -> count
REQUEST_TOTAL_SECONDS = defaultdict(float)  # (method, path) -> seconds


def record_event(event):
    EVENTS.put(event)


def metrics_worker():
    while True:
        method, path, status, duration = EVENTS.get()
        if not path.endswith("/"):
            path += "/"

        REQUEST_COUNT[(method, path, status)] += 1

        REQUEST_TOTAL_COUONT[(method, path)] += 1
        REQUEST_TOTAL_SECONDS[(method, path)] += duration * 1000


threading.Thread(target=metrics_worker, daemon=True).start()


def prometheus_metrics():
    lines = []

    # 请求总数
    lines.append("# HELP http_requests_total Total HTTP requests")
    lines.append("# TYPE http_requests_total counter")
    for (method, path, status), total in REQUEST_COUNT.items():
        lines.append(
            f'http_requests_total{{method="{method}", path="{path}", status="{status}"}} {total}'
        )

    # 请求平均耗时
    lines.append(
        "# HELP http_request_milliseconds_avg Average HTTP request in milliseconds"
    )
    lines.append("# TYPE http_request_milliseconds_avg gauge")
    for (method, path), total in REQUEST_TOTAL_SECONDS.items():
        count = REQUEST_TOTAL_COUONT[(method, path)]
        avg_time = total / count if count > 0 else 0
        lines.append(
            f'http_request_milliseconds_avg{{method="{method}", path="{path}"}} {avg_time:.6f}'
        )

    return "\n".join(lines)

