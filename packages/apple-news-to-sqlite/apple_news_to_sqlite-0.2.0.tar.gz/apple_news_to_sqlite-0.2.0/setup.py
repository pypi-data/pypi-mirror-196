# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apple_news_to_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.3.2,<14.0.0',
 'sqlite-utils>=3.30,<4.0']

entry_points = \
{'console_scripts': ['apple-news-to-sqlite = '
                     'apple_news_to_sqlite.__main__:cli']}

setup_kwargs = {
    'name': 'apple-news-to-sqlite',
    'version': '0.2.0',
    'description': 'Export "Saved Stories" from Apple News to SQLite',
    'long_description': '# apple-news-to-sqlite\n\nExport Apple News Saved Stories to SQLite\n\n## Install\n\n    pip install apple-news-to-sqlite\n\n## Source Code\n\n[apple-news-to-sqlite](https://github.com/RhetTbull/apple-news-to-sqlite)\n\n## Usage\n\n    apple-news-to-sqlite articles.db\n    \n    apple-news-to-sqlite --dump\n\n## CLI Help\n\n<!-- [[[cog\nimport cog\nfrom apple_news_to_sqlite.cli import cli\nfrom click.testing import CliRunner\nrunner = CliRunner()\nresult = runner.invoke(cli, ["--help"])\nhelp = result.output.replace("Usage: cli", "Usage: apple-news-to-sqlite")\ncog.out(\n    "```\\n{}\\n```".format(help)\n)\n]]] -->\n```\nUsage: apple-news-to-sqlite [OPTIONS] [DB_PATH]\n\n  Export your Apple News saved stories/articles to a SQLite database\n\n  Example usage:\n\n      apple_news_to_sqlite articles.db\n\n  This will populate articles.db with an "articles" table containing information\n  about your saved articles.\n\n  Note: the contents of the articles themselves are not stored in the database,\n  only metadata about the article such as title, author, url, etc.\n\nOptions:\n  --version  Show the version and exit.\n  --dump     Output saved stories to standard output\n  --schema   Create database schema and exit\n  --help     Show this message and exit.\n\n```\n<!-- [[[end]]] -->\n\n## Using apple-news-to-sqlite in your own Python code\n\n`get_saved_articles()` returns a list of dictionaries, each representing a saved article with the\nfollowing keys (all strings):\n\n    * id\n    * url\n    * title\n    * description\n    * image\n    * author\n\n```pycon\n>>> from apple_news_to_sqlite import get_saved_articles\n>>> articles = get_saved_articles()\n```\n\n## Contributing\n\nContributions of all types are welcome! Fork the repo, make a branch, and submit a PR.\n\nSee [README_DEV.md](README_DEV.md) for developer notes.\n\n## Thanks\n\nThanks to [Simon Willison](https://simonwillison.net/) who inspired this project\nwith his excellent "everything-to-sqlite" [dogsheep](https://github.com/dogsheep) project.\n\nThanks Simon also for the excellent tools\n[sqlite-utils](https://github.com/simonw/sqlite-utils) and [Datasette](https://datasette.io).\n\nThanks also to [Dave Bullock](https://github.com/eecue) who inspired this project and helped\ntremendously with the reverse engineering and initial code.\n\n## License\n\nMIT License\n',
    'author': 'Rhet Turnbull',
    'author_email': 'rturnbull+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
