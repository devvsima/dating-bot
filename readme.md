<p align="center">
  <img src="https://i.ibb.co/PGwpsJGp/Screenshot-62.png" alt="diagram" width="1200">
</p>
<details>
  <summary>📸 Screanshots</summary>

  <p align="center">
    <img src="https://i.ibb.co/ggvC6kr/Screenshot-53.png" alt="Screenshot 1" width="800">
  </p>
  <p align="center">
    <img src="https://pbs.twimg.com/media/GYKn8I_WAAAvErl?format=jpg&name=large" alt="Screenshot 2" width="800">
  </p>
  <!-- <p align="center">
    <img src="https://pbs.twimg.com/media/GYKn8I_WAAAvErl?format=jpg&name=large" alt="Screenshot 3" width="500">
  </p> -->
</details>


# 🚀 Let's get started

## 🛠️ Technology Stack
- `Aiogram 3`
- `Redis`
- `i18n`
- `Peewee`
- `PostgreSQL \ Sqlite`

---

## 📥 Installation Instructions

### 1. Clone the repository

First, clone the repository and navigate to its directory:

```bash
git clone https://github.com/devvsima/dating-bot.git
cd dating-bot
```



### 2. Setting up the virtual environment “.venv”

💡  Note: The name `.venv` can be changed to any other name you wish.

#### Linux


```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
> 💡 You may have to install apt install python3.10-venv or something like that


#### Windows


```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```


### 3. Customizing the .env environment variables

First, copy the `.env.dist` file and rename it to `.env`:

```bash
cp .env.dist .env
```

Now you need to customize the `.env` file



#### Bot Settings

| Name | Description | Example |
| -------- | -------------------------------------------------- | --------------------------- |
| TOKEN | Bot Token from [@BotFather](https://t.me/BotFather) | 1234567:ASDSFDkjdjdsedmD... |
| ADMINS | List of admin id's | 12345678,12345677 |



#### Database Setup

| Name | Description | Default |
| -------- | -------------------------------------- | ------------ |
| DB_NAME | Database Name |           |
| DB_HOST | Database Host | localhost |
| DB_PORT | Database Port | 5432 |
| DB_USER | User with access to the database ||
| DB_PASS | Database password |  |

---

### Now the bot is ready to run! 🎉
