from setuptools import setup

setup(
    name='izroq-fab-sm',
    version='0.1',
    description='Custom Izroq Security Manager for FAB Apps (Superset &amp; Airflow)',
    url='https://github.com/izroq/izroq_fab_sm',
    author='Izroq',
    install_requires=[
        'flask-appbuilder>=3.0.0',
        'authlib>=1.0.0',
    ],
    license='MIT',
    author_email='office@izroq.com',
    packages=['izroq_fab_sm'],
    zip_safe=False
)