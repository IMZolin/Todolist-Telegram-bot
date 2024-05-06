#!/bin/bash
pw_migrate migrate --database $(python _get_database_url.py) --directory ./migrations

if [ -z "$WEBHOOK_PATH" ]
then
      python main.py
else
      python webhook.py
fi