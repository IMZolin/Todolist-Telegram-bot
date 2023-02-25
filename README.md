### Todolist Telegram bot (1-st lab for API 2-nd semester, SPbPU)
Todolist Telegram bot that can create reminders (delete) with attachments, view, sort, set the date and time.
<hr>

* [Bot structure](#bot-structure)
* [Getting started](#getting-started)
    * [First steps](#first-steps)
    * [Configure environment variables](#configure-environment-variables)
        * [Bot settings](#bot-settings)
        * [Database](#database)
  * [Docker](#docker)
    * [Start bot](#start-bot)
    * [Manage bot container](#manage-bot-container)
    * [View bot logs](#view-bot-logs)
    * [Restart bot](#restart-bot)
    * [Stop bot](#stop-bot)
    * [Database postgres](#database-postgres)
        * [Manage postgres via psql](#manage-postgres-via-psql)
        * [Migrations](#migrations)
            * [Create revision](#create-revision)
            * [Upgrade database](#upgrade-database)
  
<hr>

## Bot structure
```bash
├───bin                 # some bash scripts for docker
├───bot
│   ├───filters         # some aiogram filters
│   ├───handlers
│   │   ├───errors      # error handlers
│   │   └───users       # message handlers
│   ├───keyboards
│   │   ├───default     # aiogram markups
│   │   └───inline      # aiogram inline markups
│   ├───middlewares     # aiogram middlewares
│   └───states          # aiogram states
├───data
│   ├───locales         # i18n locales
│   └───logs            # bot logs
├───models              # database models
├───services            # database services
└───utils               # some helpful things
```

## Getting started

### First steps
```bash
git clone https://github.com/IMZolin/Todolist-Telegram-bot <your project name>
cd <your project name>
pip install -r requirements.txt

# initialize database
pw_migrate migrate --database $(python _get_database_url.py) --directory ./migrations
# or if you have make you can simply type 
make db_upgrade
# run pooling
python task_handler.py
```

### Configure environment variables
Copy file `.env.dist` and rename it to `.env`
```
cp .env.dist .env
```
Than configure variables
```bash
vim .env
# or 
nano .env
```

### Bot settings:

`ADMINS` - administrators ids divided by ,
```bash
# example
ADMINS=12345678,12345677,12345676
# or one admin
ADMINS=12345678
```
`BOT_TOKEN` - bot token from [@BotFather](https://t.me/BotFather)
```bash
# example
BOT_TOKEN=123452345243:Asdfasdfasf
```
`RATE_LIMIT` - throttling rate limit (anti-spam)
```bash
# example
RATE_LIMIT=0.5 # seconds
```
### Database
Sqlite by default but if you want to use postgres you can configurate it

```bash
# Dababase postgres
DATABASE_USER=<some username>
DATABASE_PASS=<some password>
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=<some database name>
```

## Docker 
### Start bot
```bash
# grant execution rights
$ chmod +x ./bin/entrypoint.sh
$ docker-compose up -d --force-recreate
# or if you have make you can simply type 
$ make run
# or only make
$ make 
```
### Manage bot container
```bash
$ docker-compose exec bot /bin/bash
# or if you have make you can simply type 
$ make exec
```
### View bot logs
```bash
$ docker-compose logs -f bot
# or if you have make you can simply type 
$ make logs
```

### Stop bot
```bash
$ docker-compose stop
# or if you have make you can simply type 
$ make stop
```
### Database postgres
#### Manage postgres via psql
```bash
$ docker-compose exec postgres psql -U postgres postgres
# or if you have make you can simply type 
$ make psql
```
#### Migrations
##### Create revision
```bash
$ pw_migrate create --auto --database $(python _get_database_url.py) --directory ./migrations "<some revision message>"
# or if you have make you can simply type 
$ make db_revision "<some revision message>"
```
##### Upgrade database
```bash
$ pw_migrate migrate --database $(python _get_database_url.py) --directory ./migrations
# or if you have make you can simply type 
$ make db_upgrade
```