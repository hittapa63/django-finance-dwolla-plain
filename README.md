# Bundl

Vanguard for Crypto

## Installation

Setup a virtualenv and install requirements
(this example uses [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):

```bash
mkvirtualenv bundl_finance -p python3
pip install -r requirements.txt
```

## Running server

```bash
./manage.py runserver
```

## Building front-end

To build JavaScript and CSS files, first install npm packages:

```bash
npm install
```

Then to build (and watch for changes locally) just run:

```bash
npm run dev-watch
```

## Running Celery

Celery can be used to run background tasks. To run it you can use:

```bash
celery -A bundl_finance worker -l INFO
```

## Google Authentication Setup

To setup Google Authentication, follow the [instructions here](https://django-allauth.readthedocs.io/en/latest/providers.html#google).


## Running Tests

To run tests simply run:

```bash
./manage.py test
```

Or to test a specific app/module:

```bash
./manage.py test apps.utils.tests.test_slugs
```


On Linux-based systems you can watch for changes using the following:

```bash
find . -name '*.py' | entr python ./manage.py test
```

## Set key
- set Stripe API key and secret
- Dwolla key and secret
- Plain client_id and key, sandbox user credential