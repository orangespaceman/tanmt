def skip_404s(record):
    # hide 404 errors from logs
    status_code = getattr(record, 'status_code', None)
    if status_code == 404:
        return False
    return True


def skip_during_testing(record):
    # check settings module, if this is testing/ci then skip
    import os
    module = os.environ["DJANGO_SETTINGS_MODULE"]
    if module.endswith('.test') or module.endswith('.ci'):
        return False
    return True
