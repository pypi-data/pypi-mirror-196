# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flet_django',
 'flet_django.controls',
 'flet_django.management',
 'flet_django.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.0,<5.0', 'flet', 'flet-core']

setup_kwargs = {
    'name': 'flet-django',
    'version': '0.3.3',
    'description': 'Django Flutter Framework.',
    'long_description': '# Just married!!!\n# Django and Flutter.\n\n## Rapid developing db based app. Zero boilerplate code.\n\nI hate boilerplate code. I hated it all my life. I made so many steps to remove this mental parasites far from me. And now, with Flet and Django I\'m so close to get my ideal. For this moment I made as PoC a clone of a standard Flet ToDo application. All what I change is write all directly inside Django. Flet code is run directly on the backend, so we not need any dedicated communication layer. Next what I\'m done is generic data table control. This is a simple control able to create a data table for any Django model. All with searching and sorting.\n\n## Roadmap:\n* [x] Create package for a framework\n* [x] Create environment for generic Flutter app\n  * [x] GenericApp class for a new Flutter application\n  * [x] GenericPage class for a new Flutter application instance\n  * [x] GenericView class to easily create routed Flutter views\n  * [x] Generic middleware class for flexible management of Flutter view routing process\n  * [x] UrlsMiddleware class for implementing Django urls based routing\n  * [x] Generic navigation mechanism\n* [ ] Create authorisation and permissions middleware\n  * [ ] AuthApp for apps with authorization\n  * [ ] AuthMiddleware for authorisation management\n* [ ] Create generic list view for any Django model\n  * [x] Generic model\'s, data table based, control\n  * [ ] Generic form based on Django forms\n* [ ] Create generic form for any Django model\n* [ ] Manage relations between models\n* [ ] Documentation!!!\n\n## Instalation\n- Install python package:\n\n        $ pip install flet-django\n- Add \'flet_django\' to INSTALLED_APPS in settings.py:\n        `INSTALLED_APPS += [\'flet_django\']`\n\n\n## Run and usage\n\n* Let create a Django project:\n    ```bash\n    pip install Django\n    django-admin startproject test_flet_django\n    cd test_flet_django\n    python manage.py migrate\n    ```\n* Install flet and flet-django packages:\n    ```bash\n    pip install flet\n    pip install flet-django\n    ```\n* Add \'flet_django\' to INSTALLED_APPS in settings.py:\n    ```bash\n    echo "INSTALLED_APPS += [\'flet_django\']" >> test_flet_django/settings.py\n    ```\n* Create the main function in the file main_app.py at the root of your Django project:\n    ```python\n    import flet as ft\n    from flet_django.pages import GenericApp\n    main = GenericApp(controls=[ft.Text("Hello World!")])\n    ```\n* Run function __main__ from file __main_app.py__ using the Django command:\n    ```bash\n    python manage.py run_app\n    ```\n* Enjoy your desktop/mobile/web flutter app.\n\n## Flutter view\n\n- A framework based on flutter views. Flutter view is a function which takes page as a first argument, and returns instance of flet.View class.\n- For simplicity, we can use ft_view factory\n- Let create a simple flutter view example in file main_app.py:\n    ```python\n    import flet as ft\n    from flet_django.views import ft_view\n\n    def home(page):\n        return ft_view(\n            page,\n            controls=[ft.Text("Hello World!")],\n            app_bar_params=dict(title="ToDo app")\n        )\n    ```\n- Flutter view can be assigned to route by Generic App\'s urls parameter, or as a target for navigation:\n    ```python\n    import flet as ft\n    from django.urls import path\n    from flet_django.views import ft_view\n    from flet_django.pages import GenericApp\n    from flet_django.navigation import Fatum\n\n    def home(page):\n        return ft_view(\n            page,\n            controls=[ft.Text("Hello World!")],\n            app_bar_params=dict(title="ToDo app")\n        )\n\n    destinations = [\n        Fatum(\n            route="/",\n            icon=ft.icons.HOME,\n            selected_icon=ft.icons.HOME_OUTLINED,\n            label="home",\n            nav_bar=True,\n            action=True,\n            nav_rail=False\n        ),\n    ]\n\n    urlpatterns = [\n        path(\'\', home, name="home")\n    ]\n\n    main = GenericApp(\n        destinations=destinations,\n        urls=urlpatterns,\n        init_route="/"\n    )\n\n    ```\n- To run application on other devices you need establish server and build client, based on Flutter frontend project from repository\n- To run app as server use --view parameter:\n    ```bash\n    python manage.py run_app --view flet_app_hidden\n    ```\n- Server will be avaible as http server, for example:\n    ```bash\n      open http://ala.hipisi.org.pl:8085\n    ```\n- Compile ./frontend futter app to have separate ready to install application:\n    ```bash\n      cd frontend\n      flutter run --dart-entrypoint-args http://94.23.247.130:8085\n    ```\n- You can use simple script to run separate flutter application:\n    ```bash\n      python run.py\n    ```\n\n## Demo\nYou can run repository\'s project as example of usage.\nWorking demo [is here](http://ala.hipisi.org.pl:8085).\n\n## Screenshots\n\n![Android app](./todo_pixel4.png)\n\n![iOS app](./todo_iphone14.png)\n',
    'author': 'beret',
    'author_email': 'beret@hipisi.org.pl',
    'maintainer': 'Marysia Software Limited',
    'maintainer_email': 'office@marysia.app',
    'url': 'https://marysia.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
