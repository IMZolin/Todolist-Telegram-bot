pw_migrate migrate --database $(python _get_database_url.py) --directory ./migrations
python app.py