def skip_404s(record):
    # hide 404 errors from logs
    status_code = getattr(record, 'status_code', None)
    if status_code == 404:
        return False
    return True
