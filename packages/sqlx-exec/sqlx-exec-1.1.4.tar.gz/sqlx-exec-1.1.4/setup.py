import os
from setuptools import setup

# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()

long_description = read("README.rst")

setup(
    name='sqlx-exec',
    packages=['sqlexec'],
    description="sqlx-exec is a simple sql executor for Python, it help you auto manage database connection and transaction. Now support MySQL and PostgreSQL.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'DBUtils>=3.0.0',
    ],
    version='1.1.4',
    url='https://gitee.com/summry/sql-exec',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['sql', 'MySQL', 'PostgreSQL', 'python'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.5',
    zip_safe=False
)

