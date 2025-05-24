<p align="center">
  <img src="./images/rounded_logo.png" alt="diagram" width="150">
</p>
<h1 align="center" style="border-bottom: none">
    <b>
        <a href="https://t.me/michalangelo_bot?start=Oj0wd">Michelangelo</a><br>
    </b>
    Telegram dating bot 💞<br>
</h1>

---

<p align="center">
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/aiogram-3.x-blueviolet" alt="Aiogram"/>
  <img src="https://img.shields.io/badge/database-PostgreSQL-lightblue" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/storage-Redis-red" alt="Redis"/>
  <img src="https://img.shields.io/badge/license-CC%20BY--NC%204.0-green" alt="License"/>
</p>

Hi, I made my own telegram dating bot, I hope it will be useful for someone. If you want to support me, you can put a star on the repository ; )


<p align="center">
  <img src="./images/preview.png" alt="screenshot 1" width="1000"/>

</p>


## Navigation

- [Navigation](#navigation)
- [Features](#features)
- [Technical Features](#technical-features)
- [Install](#install)
  - [Settings](#settings)
    - [Bot](#bot)
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
### Settings

First, copy the `.env.dist` file and rename it to `.env`:
Now you need to customize the `.env` file
#### Bot

| <center>Name</center> | <center>Description</center>                                                  | <center>Example</center> |
| --------------------- | ----------------------------------------------------------------------------- | ------------------------ |
| TOKEN                 | Bot Token from [@BotFather](https://t.me/BotFather)                           | 1234567:ASDSFDkjdjdsedmD |
| ADMINS                | List of administrator id's                                                    | 2345678,12345677         |
| MODERATOR_GROUP_ID    | (Optional) ID of the administrator group, where user complaints will be sent. | -100123456789            |
| SKIP_UPDATES          | Option whether the bot will skip updates while not active                     | True, False              |

#### Database
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

#### Migrations

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


#### Redis
The radishes will be used as FSM storage. If redis is not connected the standard aiogram storage will be used.
You can specify a link to the Redis connection in the `RD_URL` field at once.

| <center>Name</center> | <center>Description</center>                   | <center>Example</center> |
| --------------------- | ---------------------------------------------- | ------------------------ |
| REDIS_HOST            | Database host                                  | localhost                |
| REDIS_PORT            | Database port                                  | 6379                     |
| REDIS_DB              | Database name                                  | 5                        |
| RD_URL                | (Optional)Full link to connect to the database | redis://localhost:6379/5 |

#### Localization
The bot has localization for 6 languages: en, ru, uk, fr, pl, es

- Collecting all the texts from the project
```bash
pybabel extract --input-dirs=. -o data/locales/bot.pot --project=bot
```

- Create files with translations into different languages
```bash
pybabel init -i data/locales/bot.pot -d data/locales -D bot -l en
pybabel init -i data/locales/bot.pot -d data/locales -D bot -l ru
pybabel init -i data/locales/bot.pot -d data/locales -D bot -l uk
pybabel init -i data/locales/bot.pot -d data/locales -D bot -l fr
pybabel init -i data/locales/bot.pot -d data/locales -D bot -l pl
pybabel init -i data/locales/bot.pot -d data/locales -D bot -l es
```


- Once all the texts are translated, you need to compile all the translations
```bash
pybabel compile -d data/locales -D bot --statistics
```

```bash
pybabel update -i data/locales/bot.pot -d data/locales -D bot
```

---

### Startup

First you need to [install dependencies](#Install) and do a [database migration](#Migrations) if you haven't already done one.

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

python main.py
```

> 💡 You may have to install apt install python3.10-venv or something like that.

#### UV

```bash
uv sync
uv run main.py
```

---

## License

This project is licensed under the **Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. See the [LICENSE](./LICENSE) file for details.
