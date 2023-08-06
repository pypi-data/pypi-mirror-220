from setuptools import setup

setup(
    name='gptree',
    version='0.1',
    py_modules=['gptree'],
    install_requires=[
        'streamlit',
        'openai',
    ],
    entry_points='''
        [console_scripts]
        gptree=gptree:cli
    ''',
)
