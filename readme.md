# <center>Telegram dating bot [Michelangelo](https://t.me/michalangelo_bot?start=Oj0wd) 💞</center>
- `Aiogram 3`
- `i18n`
- `SqlAlchemy`
- `Matplotlib`, `Geopy`
- `Redis`,` PostgreSQL \ Sqlite, `
<p align="center">

  <img src="https://i.ibb.co/PGwpsJGp/Screenshot-62.png" alt="diagram" width="1100">

</p>

---
## Navigation

- [Telegram dating bot Michelangelo 💞](#telegram-dating-bot-michelangelo-)
  - [Navigation](#navigation)
  - [Install](#install)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Settings](#settings)
    - [Bot](#bot)
    - [Database](#database)
    - [Redis](#redis)
  - [Migrations](#migrations)
  - [Startup](#startup)

---
## Install
First you need to bend the repository to the correct derictory.

```bash
git clone https://github.com/devvsima/dating-bot.git
cd dating-bot
```
### Windows

```bash
python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt
```
### Linux

```bash
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

> 💡 You may have to install apt install python3.10-venv or something like that.

---
## Settings

First, copy the `.env.dist` file and rename it to `.env`:
Now you need to customize the `.env` file
### Bot

| <center>Name</center> | <center>Description</center>                                                  | <center>Example</center> |
| --------------------- | ----------------------------------------------------------------------------- | ------------------------ |
| TOKEN                 | Bot Token from [@BotFather](https://t.me/BotFather)                           | 1234567:ASDSFDkjdjdsedmD |
| ADMINS                | List of administrator id's                                                    | 2345678,12345677         |
| MODERATOR_GROUP_ID    | (Optional) ID of the administrator group, where user complaints will be sent. | -100123456789            |
| SKIP_UPDATES          | Option whether the bot will skip updates while not active                     | True, False              |

### Database
If the settings for the database are not filled out, asynchronous Sqlite will be used.
You can specify a link to the database connection in the DB_URL field.

| <center>Name</center> | <center>Description</center>                   | <center>Example</center>                               |
| --------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| DB_NAME               | Database name                                  | 1234567:ASDSFDkjdjdsedmD                               |
| DB_HOST               | Database host                                  | 2345678,12345677                                       |
| DB_PORT               | Database port                                  | -100123456789                                          |
| DB_USER               | Database owner                                 | True, False                                            |
| DB_PASS               | Database password                              | postgresql                                             |
| DB_URL                | (Optional)Full link to connect to the database | postgresql+asyncpg://user:password@localhost:port/name |


### Redis
The radishes will be used as FSM storage. If redis is not connected the standard aiogram storage will be used.
You can specify a link to the Redis connection in the `RD_URL` field at once.

| <center>Name</center> | <center>Description</center>                   | <center>Example</center> |
| --------------------- | ---------------------------------------------- | ------------------------ |
| REDIS_HOST            | Database host                                  | localhost                |
| REDIS_PORT            | Database port                                  | 6379                     |
| REDIS_DB              | Database name                                  | 5                        |
| RD_URL                | (Optional)Full link to connect to the database | redis://localhost:6379/5 |

---

## Migrations

This project uses **Alembic** for database migrations.

- **Create a new migration:**

    ```sh
    alembic revision --autogenerate -m "Migration description"
    ```

- **Apply migrations:**

    ```sh
    alembic upgrade head  # Apply all new migrations
    alembic upgrade "migration_name"  # Apply a specific migration
    ```

- **Rollback migrations:**

    ```sh
    alembic downgrade base  # Reset database to the initial state
    alembic downgrade "migration_name"  # Rollback to a specific migration
    ```


Ensure `alembic.ini` has the correct database URL before running migrations.


---
## Startup

First you need to [install dependencies](#Install) and do a [database migration](#Migrations) if you haven't already done one.

```bash
python main.py
```
