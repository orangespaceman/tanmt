# TANMT - Deployment

[&laquo; Back](../README.md)

How to deploy the app


## Deployment

* Set up a server, e.g. on [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04)

    - Note: When creating `gunicorn.service` file, the following needs to be added:

      ```
      --env DJANGO_SETTINGS_MODULE=tanmt.settings.production
      ```

* Check out this project

* Install requirements:

  ```
  pip install -r production.txt
  ```

* Install [nodejs and npm](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04)

* Install front-end dependencies:

  ```
  npm install
  ```

* Run frontend build:

  ```
  npm run build
  ```

* Optional: manually upload any existing media files, into `/tanmt/media`

* Manually create settings files - `/tanmt/tanmt/settings/production.py` - using the sample files in that directory

* Collect static assets:

  ```
  manage.py collectstatic  --settings=tanmt.settings.production
  ```

* Migrate DB:

  ```
  manage.py migrate  --settings=tanmt.settings.production
  ```

* Optional: manually (generate, upload and) load fixture data:

  ```
  manage.py loaddata foo bar
  ```

### Deployment - making updates:

 - Push to repo, wait for tests to complete
 - Log into server

    ```
    cd tanmt/
    git pull -p
    npm run build
    source env/bin/activate
    pip install -r requirements/production.txt
    cd tanmt/
    python manage.py migrate --settings=tanmt.settings.production
    python manage.py collectstatic --settings=tanmt.settings.production
    python manage.py loaddata foo bar --settings=tanmt.settings.production
    sudo systemctl restart gunicorn
    sudo systemctl restart nginx
    ```
