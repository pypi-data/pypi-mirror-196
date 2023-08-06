# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_webapp_auth']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'telegram-webapp-auth',
    'version': '0.1.0',
    'description': '',
    'long_description': '# telegram-webapp-auth\nThis Python package implements [Telegram Web authentication algorithm](https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app).\n\n## Documentation\n[Small package - small documentation](docs/auth.md) :)\n\n## Examples\n### Using with FastAPI\nLet\'s create some useful stuff according [OAuth2 tutorial](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/?h=auth).\n\nFile `utils.py`:\n```python\nfrom telegram_webapp_auth import parse_user_data, parse_init_data, validate\nfrom fastapi import HTTPException, Depends\nfrom fastapi.security.http import HTTPBase, HTTPAuthorizationCredentials\nfrom pydantic import BaseModel\n\nfrom .config import TelegramBotSettings  # Telegram Bot configuration\n\ntelegram_authentication_schema = HTTPBase()\n\n\nclass TelegramUser(BaseModel):\n    id: int\n    first_name: str\n    last_name: str\n    username: str\n    language_code: str\n\n\ndef verify_token(auth_cred: HTTPAuthorizationCredentials) -> TelegramUser:\n    settings = TelegramBotSettings()\n    init_data = auth_cred.credentials\n    try:\n        if validate(init_data, settings.secret_key):  # generated using generate_secret_key function\n            raise ValueError("Invalid hash")\n    except ValueError:\n        raise HTTPException(status_code=403, detail="Could not validate credentials")\n\n    init_data = parse_init_data(init_data)\n    user_data = parse_user_data(init_data["user"])\n    return TelegramUser.parse_obj(user_data)\n\n\ndef get_current_user(\n    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema)\n) -> TelegramUser:\n    return verify_token(auth_cred)\n```\n\nFinally, we can use it as usual.\n\nFile `app.py`:\n```python\nfrom pydantic import BaseModel\nfrom fastapi import FastAPI, Depends\n\nfrom utils import get_current_user, TelegramUser\n\napp = FastAPI()\n\nclass Message(BaseModel):\n    text: str\n\n\n@app.post("/message")\nasync def send_message(\n    message: Message,\n    user: TelegramUser = Depends(get_current_user),\n):\n    """\n    Some backend logic...\n    """\n    ...\n```\n',
    'author': 'Dmitry Vasiliev',
    'author_email': 'contact.vasiliev.dmitry@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
