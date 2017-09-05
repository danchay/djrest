from disutils.core import setup

setup(
    name='todo_api',
    version='0.1',
    description='A ToDo List API built w/ Django REST Framework',
    author='Dan Chay',
    author_email='danchay@gmail.com',
    url='https://github.com/danchay/djrest.git',
    packages=find_packages(),
    install_requires=[
    Django==1.11.4,
    djangorestframework==3.6.4,
    pytz==2017.2,
    ]
    )
