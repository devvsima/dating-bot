<p align="center">
  <img src="./images/rounded_logo.png" alt="diagram" width="150">
</p>
<h1 align="center" style="border-bottom: none">
    <b>
        <a href="https://t.me/michalangelo_bot?start=git_Oj0wd">Michelangelo</a><br>
    </b>
    Telegram dating bot 💞<br>
</h1>

<b> Hi, I made my own telegram dating bot, I hope it will be useful for someone. If you want to support me, you can put a star on the repository ; ) </b>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/aiogram-3.x-blueviolet" alt="Aiogram"/>
  <img src="https://img.shields.io/badge/database-PostgreSQL-lightblue" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/storage-Redis-red" alt="Redis"/>
  <img src="https://img.shields.io/badge/license-CC%20BY--NC%204.0-green" alt="License"/>
</p>

<p align="center">
  <img src="./images/new_preview.png" alt="screenshot 1" width="1000"/>

</p>

---

## Navigation

- [Navigation](#navigation)
- [Features](#features)
- [Technical Features](#technical-features)
- [Install](#install)
- [Settings](#settings)
  - [Bot](#bot)
  - [Search](#search)
  - [Webapp](#webapp)
  - [Database](#database)
  - [Migrations](#migrations)
  - [Redis](#redis)
  - [Localization](#localization)
- [Startup](#startup)
  - [Windows](#windows)
  - [Linux](#linux)
  - [UV](#uv)
- [License](#license)

---

## Features

- 🌍 **Languages**: Localization into different languages: English, Russian, Ukrainian, Spanish, French, Polish
- 💬 **Matchmaking**: Helps users find each other based on shared interests.
- 🔒 **Secure**: Implements secure data handling and user privacy.

---

## Technical Features

- 🌍 **Geolocation**: Uses `Geopy` to determine user locations.
- 📊 **Analytics**: Generates visual graphs with `Matplotlib`.
- 🗂️ **Multilingual Support**: Supports multiple languages via `i18n`.
- ⚡ **High Performance**: Utilizes `Redis` for FSM storage and `PostgreSQL` for database operations.

---

## Install

First you need to bend the repository to the correct derictory.

```bash
git clone https://github.com/devvsima/dating-bot.git
cd dating-bot
```

---

## Settings

First, copy the `.env.dist` file and rename it to `.env`:
Now you need to customize the `.env` file

### Bot

| <center>**Name**</center> | <center>**Description**</center>                                                     | <center>**Example**</center>      |
| ------------------------- | ------------------------------------------------------------------------------------ | --------------------------------- |
| TELEGRAM_BOT_TOKEN        | Bot Token from [@BotFather](https://t.me/BotFather)                                  | 1234567:ASDSFDkjdjdsedmD          |
| SKIP_UPDATES              | Skip requests that were sent while the bot was not working                           | False                             |
| SET_COMMANDS              | Set commands when starting the bot                                                   | True                              |
| RATE_LIMIT                | Number of requests                                                                   | 2                                 |
| TIME_WINDOW               | Time interval between requests                                                       | 1                                 |
| ADMINS                    | List of administrator IDs separated by commas                                        | 123456789, 987654321              |
| BOT_CHANNEL_URL           | (Optional) The bot channel he will be sending to                                     | https://t.me/michalangelo_channel |
| MODERATOR_GROUP_ID        | (Optional) ID of the moderator group where complaints and notifications will be sent | -100234567891                     |
| NEW_USER_ALET_TO_GROUP    | (Optional) Send notifications to the moderator group                                 | True                              |

### Search

Configuring user profile search

| <center>**Search**</center> | <center>**Description**</center>                                        | <center>**Example**</center> |
| --------------------------- | ----------------------------------------------------------------------- | ---------------------------- |
| INITIAL_DISTANCE            | Initial search distance                                                 | 200.0                        |
| MAX_DISTANCE                | Maximum search distance                                                 | 1500.0                       |
| RADIUS_STEP                 | Distance increase step                                                  | 200.0                        |
| MIN_PROFILES                | Minimum number of profiles for search                                   | 100                          |
| BLOCK_SIZE                  | Size of profile batches in search (needed for randomizing profiles)     | 15.0                         |
| AGE_RANGE_MULTIPLIER        | Age search multiplier (the older the person, the greater the age range) | 0.20                         |
| MIN_AGE_RANGE               | Minimum age difference                                                  | 2                            |
| MAX_AGE_RANGE               | Maximum age difference                                                  | 15                           |

### Webapp

| <center>**Name**</center> | <center>**Description**</center>                                 | <center>**Example**</center>                                         |
| ------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------- |
| WEBAPP_HOST               | Website host                                                     | localhost                                                            |
| WEBAPP_PORT               | Website port                                                     | 8080                                                                 |
| WEBAPP_DOMEN              | Website domain                                                   | [michalangelo.com](https://devvsima.github.io/michalangelo-landing/) |
| WEBAPP_URL                | (Optional) Direct link, if specified, will be used as a priority | https://devvsima.github.io/michalangelo-landing/                     |

### Database

If the settings for the database are not filled out, asynchronous Sqlite will be used.
You can specify a link to the database connection in the DB_URL field.

| <center>**Name**</center> | <center>**Description**</center>                                 | <center>**Example**</center> |
| ------------------------- | ---------------------------------------------------------------- | ---------------------------- |
| DB_NAME                   | Database name                                                    | michalangelo                 |
| DB_HOST                   | Database host                                                    | localhost                    |
| DB_PORT                   | Database port                                                    | 5432                         |
| DB_USER                   | User with Database permissions                                   | postgres                     |
| DB_PASS                   | Password from user                                               | bestpass                     |
| DB_URL                    | (Optional) Direct link, if specified, will be used as a priority | postgresql+asyncpg://...@... |
| ECHO                      | Logging of all SQL queries                                       | False                        |
| POOL_SIZE                 | Number of sessions                                               | 12                           |
| MAX_OVERFLOW              | Number of additional sessions                                    | 18                           |

### Migrations

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

### Redis

The radishes will be used as FSM storage. If redis is not connected the standard aiogram storage will be used.
You can specify a link to the Redis connection in the `RD_URL` field at once.

| <center>**Name**</center> | <center>**Description**</center>                                 | <center>**Example**</center> |
| ------------------------- | ---------------------------------------------------------------- | ---------------------------- |
| REDIS_HOST                | Redis host                                                       | localhost                    |
| REDIS_PORT                | Redis host                                                       | 6379                         |
| REDIS_PASS                | (Optional) Redis password                                        | bestpass                     |
| REDIS_DB                  | Database number                                                  | 1                            |
| RD_URL                    | (Optional) Direct link, if specified, will be used as a priority | redis://...@...              |

### Localization

The bot has localization for 6 languages: en, ru, uk, fr, pl, es

- Collecting all the texts from the project

```bash
pybabel extract --input-dirs=. -o locales/bot.pot --project=bot
```

- Create files with translations into different languages

```bash
pybabel init -i locales/bot.pot -d locales -D bot -l en
pybabel init -i locales/bot.pot -d locales -D bot -l ru
pybabel init -i locales/bot.pot -d locales -D bot -l uk
pybabel init -i locales/bot.pot -d locales -D bot -l fr
pybabel init -i locales/bot.pot -d locales -D bot -l pl
pybabel init -i locales/bot.pot -d locales -D bot -l es
```

- Once all the texts are translated, you need to compile all the translations

```bash
pybabel compile -d locales -D bot --statistics
```

```bash
pybabel update -i locales/bot.pot -d locales -D bot
```

## Startup

First you need to [install dependencies](#Install) and do a [database migration](#Migrations) if you haven't already done one.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

python main.py
```

> 💡 You may have to install apt install python3.10-venv or something like that.

### UV

```bash
uv sync
uv run main.py
```

---

## License

This project is licensed under the **Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. See the [LICENSE](./LICENSE) file for details.
