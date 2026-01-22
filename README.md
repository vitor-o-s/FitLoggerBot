# FitLoggerBot
A bot to help your understand and plan your trains

## How to Contribute

If you are new to Python development here are some initial steps.

First, the library used to develop this bot is [python-telegram-bot](https://docs.python-telegram-bot.org/en/v20.8/index.html). A basic bot tutorial is provided [here](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot).

Second, as seen, the bot needs a token (this has already been generated) to add to your system (linux, bash) use the following command:

**Attention - Never put the token directly in the code**
```bash
nano ~/.bashrc
export TELEGRAM_BOT_TOKEN="" 
source ~/.bashrc
```

Third, create a virtual environment to isolate your packages. You can do this in the following way:

```bash
python -m venv .venv
```

After creating venv, you must activate it with the following command:

```bash
source ./.venv/bin/activate
```

With venv activated, install the packages necessary for project development using the requirements.txt file, it contains a list of packages and versions used

```bash
pip install requirements.txt
```

To run the bot just call de main.py file

```bash
python main.py
```

If you want to change projects or stop developing. Deactivate your virtual environment

```bash
deactivate
```

When developing a project it is important that a standard is followed. Python follows the standard proposed in [PEP-8](https://pep8.org/). It is not necessary to memorize all the rules but you will eventually remember some. In this project we use a tool called [blue](https://blue.readthedocs.io/en/latest/) that implements this pattern and automatically corrects it for us. Try using the following command before submitting a fix package.

```bash
blue .
```

Finally, I recommend separating the contributions. A short PR is easier to review, adjust and merge