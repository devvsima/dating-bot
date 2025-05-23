# <center>Telegram dating bot [Michelangelo](https://t.me/michalangelo_bot?start=Oj0wd) 💞</center>

![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-green)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-blueviolet)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-lightblue)
![Redis](https://img.shields.io/badge/storage-Redis-red)

As support, you can put ⭐️ on the repository =)

<p align="center">
  <img src="./images/logo.png" alt="diagram" width="512" height="512">
</p>


---

## Navigation

- [Telegram dating bot Michelangelo 💞](#telegram-dating-bot-michelangelo-)
  - [Navigation](#navigation)
  - [Features](#features)
  - [Install](#install)
    - [Windows](#windows)
    - [Linux](#linux)
    - [UV](#uv)
  - [Settings](#settings)
    - [Bot](#bot)
    - [Database](#database)
      - [Migrations](#migrations)
    - [Redis](#redis)
    - [Localization](#localization)
  - [Startup](#startup)
    - [Python](#python)
    - [UV run](#uv-run)
  - [Contributing](#contributing)
  - [License](#license)

---

## Features

- 💬 **Matchmaking**: Helps users find each other based on shared interests.
- 🌍 **Geolocation**: Uses `Geopy` to determine user locations.
- 📊 **Analytics**: Generates visual graphs with `Matplotlib`.
- 🗂️ **Multilingual Support**: Supports multiple languages via `i18n`.
- ⚡ **High Performance**: Utilizes `Redis` for FSM storage and `PostgreSQL` for database operations.
- 🔒 **Secure**: Implements secure data handling and user privacy.

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

> 💡 You may have to install apt install python3.10-venv or something like that.
```
### UV

```bash
uv sync
```

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


### Redis
The radishes will be used as FSM storage. If redis is not connected the standard aiogram storage will be used.
You can specify a link to the Redis connection in the `RD_URL` field at once.

| <center>Name</center> | <center>Description</center>                   | <center>Example</center> |
| --------------------- | ---------------------------------------------- | ------------------------ |
| REDIS_HOST            | Database host                                  | localhost                |
| REDIS_PORT            | Database port                                  | 6379                     |
| REDIS_DB              | Database name                                  | 5                        |
| RD_URL                | (Optional)Full link to connect to the database | redis://localhost:6379/5 |

### Localization
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

## Startup

First you need to [install dependencies](#Install) and do a [database migration](#Migrations) if you haven't already done one.

### Python
```bash
python main.py
```

### UV run
```bash
uv run main.py
```
---

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m "Add your feature"`.
4. Push your changes: `git push origin feature/your-feature-name`.
5. Create a Pull Request.

Please ensure your code adheres to the project's style and passes all tests.

---

## License

This project is licensed under the **Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. See the [LICENSE](./LICENSE) file for details.
