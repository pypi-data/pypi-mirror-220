from distutils.core import setup

REQUIREMENTS = [
    'pydantic',
    'transformers',
    'nltk',
    'rouge-score',
    "openai",
]

setup(
    name='entail',
    version='0.0.4',
    description='Python Distribution Utilities',
    author='Hao Wu',
    author_email='haowu@dataset.sh',
    url='',
    packages=['entail'],
    install_requires=REQUIREMENTS
)
