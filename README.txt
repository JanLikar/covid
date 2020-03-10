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

    - Generate your first revision.

        venv/bin/alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

        venv/bin/alembic -c development.ini upgrade head

- Load default data into the database using a script.

    venv/bin/initialize_back_db development.ini

- Run your project's tests.

    venv/bin/pytest

- Run your project.

    venv/bin/pserve development.ini
