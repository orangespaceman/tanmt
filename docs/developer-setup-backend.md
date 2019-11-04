# TANMT - Developer setup - Backend

[&laquo; Back](../README.md)

How to install the app locally.


## Requirements

* Python 3
* PostgreSQL


Once you have cloned this repo, run through the following steps:


## Python

This project has been developed in Python 3.6.5 - to check what version of Python you are running in your console run:

```
python --version
python3 --version
```

Please install Python 3.6.5 if you do not have it. We suggest using [pyenv](https://github.com/pyenv/pyenv) to manage python versions easily.


### Install pyenv using Homebrew

```
brew update
brew install pyenv
```

Add the following to your `.bash_profile` and reload terminal session:

```
eval "$(pyenv init -)"
```


### Install Python 3.6.5 with pyenv

```
pyenv install 3.6.5
```


### Virtualenv

When developing Python apps a virtual environment can be used to keep all your dependencies sandboxed for just this project.

First, install `virtualenv`:

```
pip install virtualenv
```

Create the virtualenv:

```
virtualenv env --python=$HOME/.pyenv/versions/3.6.5/bin/python
```

To activate the virtualenv, run:

```
source env/bin/activate
```


### Installing requirements

Python dependencies are installed using `pip`. This project uses `pip-tools` to help manage dependencies.

- Pip tools: https://github.com/jazzband/pip-tools

Install pip-tools:

```
pip install pip-tools
```

Install local dependencies, via the local.txt requirements file (this includes base and test requirements):

```
cd requirements && pip-sync local.txt
```

### Adding a new dependency

Add dependency to corresponding `.in` in the requirements directory file and then run:

```
cd requirements && make all
```

Then run `pip-sync` again:

```
pip-sync local.txt
```


## PostGres

This project requires PostgreSQL 9.4+ to support some features.

The easiest way to install PostgresSQL on macOS is to use [Postgresapp](http://postgresapp.com/). Make sure you download the version running Postgres 9.4 and follow installation instructions on the Posgresapp site.

You can either run `psql` from a terminal, or select 'open psql' from the menu if you click on the icon in the macOS menu bar

Once you have opened `psql`, create a database for the project:

```
CREATE DATABASE tanmtdb;
CREATE USER tanmtuser WITH PASSWORD 'tanmtpw';
GRANT ALL PRIVILEGES ON DATABASE tanmtdb TO tanmtuser;
```

A few other useful psql commands...

To list databases:

```
\l
```

To select a database:

```
\c [database name]
```

List tables:

```
\d
\dt
```

Note: To quit the psql shell use `\q`
