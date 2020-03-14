back
====

Getting Started
---------------

- Change directory into your newly created project.

    cd back

- Create a Python virtual environment.

    python3 -m venv venv

- Upgrade packaging tools.

    venv/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    venv/bin/pip install -e ".[testing]"

- Initialize and upgrade the database using Alembic.

    - Upgrade alembic revision.

        venv/bin/alembic -c development.ini -x url="sqlite:///back.sqlite" upgrade head

    - If you need to generate your first revision.

        venv/bin/alembic -c development.ini -x url="sqlite:///back.sqlite" revision --autogenerate -m "init"


    - Adding new revision, just omit the --autogenerate

- Load default data into the database using a script.

    venv/bin/initialize_back_db development.ini

- Run your project's tests.

    venv/bin/pytest

- Run your project.

    venv/bin/pserve development.ini


Locale
------

- Adding new entries to translation:

    cd back/locale
    vim messages.pot # add new entry

    msgfmt -o back/locale/en/LC_MESSAGES/messages.mo back/locale/en/LC_MESSAGES/messages.po