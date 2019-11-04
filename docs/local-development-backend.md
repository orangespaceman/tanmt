# TANMT - Local development - Backend

[&laquo; Back](../README.md)

How to start the app locally for day-to-day development work.

## Virtualenv

Start the virtualenv:

```
source env/bin/activate
```


## Dependencies

Ensure you have the latest dependencies:

```
cd requirements && pip-sync local.txt
```

## Run the app

- Move from the root directory to the `tanmt` directory:

  ```
  cd tanmt
  ```

- Run database migrations:

  ```
  python manage.py migrate
  ```

- Start server:

  ```
  python manage.py runserver
  ```

  or

  ```
  django-admin runserver --pythonpath=. --settings=tanmt.settings.local
  ```

- Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser

- To see the admin area, open [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) in a browser

### Content population

- You can automatically populate the site with data using the following command:

  ```
  python3 manage.py loaddata foo bar
  ```

## Development

### Linting

The code is linted with flake8.

To lint the backend code in a terminal window:

```
flake8
```

Imports are ordered by isort.

To check for isort errors in a terminal window:

```
isort --check-only --quiet --recursive --diff tanmt

```

To fix reported isort errors:

```
isort --quiet --recursive .
```

Code is auto-formatted with yapf.

To check for yapf formatting errors in a terminal window:

```
yapf --diff --recursive --exclude=*migrations* tanmt
```

### Tests

To test the backend code:

```
pytest
```

### Pre-commit hooks

To add yapf, flake8 and isort as git pre-commit hooks, run the following command:

```
pre-commit install
```

### VS Code

If you use VS Code, the code will automatically be linted in-editor
