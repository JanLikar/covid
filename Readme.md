# COVID-19 Tracker
A map that allows people with COVID-19 to mark their past locations to warn others that might have come into contact with them.


![A screenshot of the app](screenshot.png)

[Demo / staging](https://covid-staging.herokuapp.com/)


## Seting up local environment
The app is written in Python, using Pyramid framework.

We use virtualenvs and docker-compose to simplify development.

First, create a virtual environment.

    python3 -m venv venv

Install the Python dependencies.

    venv/bin/pip install -e ".[testing]"


If psycopg2 install fails, you might have some build dependencies missing. A possible workaround is to replace psycopg2 with psycopg2-binary.

Run

    docker-compose up -d

to setup a PostgreSQL database.

Then you must migrate the DB using

    venv/bin/alembic -c development.ini upgrade head

(The -x argument is a hack, the connection string should ideally be taken from development.ini. See #58.)

To load some sample data, run the following:

    venv/bin/initialize_back_db development.ini

Run the development server with

    venv/bin/pserve development.ini


### DB migrations
    venv/bin/alembic -c development.ini revision --autogenerate -m "init"

### Translations
After modifyning translation files, they need to be compiled from .mo to .po.

    msgfmt -o back/locale/en/LC_MESSAGES/messages.mo back/locale/en/LC_MESSAGES/messages.po


#### Adding translatable strings
    cd back/locale
    vim messages.pot # add new entry
    vim back/locale/en/LC_MESSAGES/messages.mo

#### Adding new translations
Change XX into the desired locale name.

    cp back/locale/messages.pot back/locale/XX/LC_MESSAGES/messages.po


## Contributing
Pull requests are kindly accepted. Please assign yourself to a ticket, before starting.

Your branch should be based on the staging branch. After merging to staging, the branch gets automatically deployed to [https://covid-staging.herokuapp.com/](https://covid-staging.herokuapp.com/).

When testing is completed, we pull the changes into master, which gets deployed to production.

