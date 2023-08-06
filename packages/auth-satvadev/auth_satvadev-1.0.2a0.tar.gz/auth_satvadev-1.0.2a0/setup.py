# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['auth_satvadev', 'auth_satvadev.api', 'auth_satvadev.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.0,<5.0.0',
 'celery>=5.2.3,<6.0.0',
 'django-celery-beat>=2.2.1,<3.0.0',
 'django-celery-results>=2.2.0,<3.0.0',
 'djangorestframework-simplejwt>=4.8.0,<5.0.0',
 'mail-satvadev>=1.0.6,<2.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'sentry-sdk>=1.5.6,<2.0.0',
 'uWSGI>=2.0.20,<3.0.0']

setup_kwargs = {
    'name': 'auth-satvadev',
    'version': '1.0.2a0',
    'description': 'Registration with confirmation by code and token authorization',
    'long_description': "# Django приложение аутентификации\n\n## Конфигурация\nПодключение приложения\n```python\nINSTALLED_APPS = [\n    'auth_satvadev',\n]\n```\n\n## Использование классов аутентификации\nДля использования необходимо задать переменную в settings.py:\n```python\nSENDER_CLASS = 'SenderClassName'\n```\n, где SenderClassName название класса для отправления и валидации кода подтверждения из списка:\n```\n'MailSender',\n```\n\nТакже, необходимо добавить URL's аутентификации в urls.py проекта:\n```python\nurlpatterns = [\n    ...\n    path(\n        'api/auth-satvadev/',\n        include(('auth_satvadev.api.urls', 'auth_satvadev'))\n    ),\n    ...\n]\n```\n\nДля запросов авторизации используются пути:\n    'api/auth-satvadev/jwt/' - для получения JWT токена\n    'api/auth-satvadev/jwt/refresh/' - обновления JWT токена\n    'api/auth-satvadev/reset-password/' - для запроса на восстановление пароля\n    'api/auth-satvadev/reset-password/confirm/' - для проверки кода подтверждения\n",
    'author': 'satva.dev',
    'author_email': 'info@satva.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.10,<4.0.0',
}


setup(**setup_kwargs)
