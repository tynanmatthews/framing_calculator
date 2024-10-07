# Frameit

A django project that includes an app for running a picture framing store.

# Useful commands

To enter the python virtual environment, navigate to the root of the directory, then,
```bash
source .venv/bin/activate
```

Once you have done this you can execute other python commands.
Django has a bunch of built in helpful tools in the manage.py file in the root of this directory.
Some useful ones ...

Running the dev server
```bash
python3 manage.py runserver
```

Making new database migrations
```bash
python3 manage.py makemigrations frameit
```

Migrating
```bash
python3 manage.py migrate
```
