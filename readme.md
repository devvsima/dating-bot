Technologies stacj used: peewee, aiogram2, postgresql

<hr>

# Getting start
## How to install?
### Clone

```bash
git clone https://github.com/devSimaa/michelangelo-bot
cd michelangelo-bot
```
### Virtual environments ".venv"

Linux:
pip3 install -r requirements.txt
```bash
python3 -m venv .venv
source .venv\bin\activate
```
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
`.venv` you can change it to another name


### Configure environment variables
Copy file `.env.dist` and rename it to `.env`
```
$ cp .env.dist .env
```
Than configure variables
```bash
$ vim .env
# or 
$ nano .env
```
### Bot settings:

`ADMINS` - administrators ids
```bash
# example
ADMINS=12345678,12345677,12345676

```
`TOKEN` - bot token from [@BotFather](https://t.me/BotFather)
```bash
# example
BOT_TOKEN=123452345243:Asdfasdfasf
```
Dababase postgres
`DB_NAME` - database name
`DB_HOST` - database host | default='localhost'
`DB_PORT` - database port | default=5432
`DB_USER` - user with access to the database
`DB_PASS` - database password
