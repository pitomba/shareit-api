def apply_headers(handler, headers):
    for header in headers:
        handler.set_header(*header)
