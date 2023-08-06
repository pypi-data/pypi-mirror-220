# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sweepai',
 'sweepai.app',
 'sweepai.core',
 'sweepai.handlers',
 'sweepai.utils',
 'sweepai.utils.config']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.31,<4.0.0',
 'PyGithub==1.58.2',
 'config-path>=1.0.3,<2.0.0',
 'gradio>=3.35.2,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'typer>=0.9.0,<0.10.0',
 'urllib3<2.0.0']

entry_points = \
{'console_scripts': ['sweep = sweepai.app.cli:app',
                     'sweepai = sweepai.app.cli:app']}

setup_kwargs = {
    'name': 'sweepai',
    'version': '0.5.2',
    'description': 'Sweep software chores',
    'long_description': '<p align="center">\n    <img src="https://github.com/sweepai/sweep/assets/26889185/39d500fc-9276-402c-9ec7-3e61f57ad233">\n</p>\n<p align="center">\n    <i>Bug Reports & Feature Requests ⟶&nbsp; Code Changes</i>\n</p>\n\n<p align="center">\n<a href="https://sweep.dev">\n    <img alt="Landing Page" src="https://img.shields.io/badge/Site-sweep.dev-blue?link=https%3A%2F%2Fsweep.dev">\n</a>\n<a href="https://docs.sweep.dev/">\n    <img alt="Docs" src="https://img.shields.io/badge/Docs-docs.sweep.dev-blue?link=https%3A%2F%2Fdocs.sweep.dev">\n</a> \n<a href="https://discord.gg/sweep-ai">\n    <img src="https://dcbadge.vercel.app/api/server/sweep-ai?style=flat" />\n</a>\n<img alt="PyPI" src="https://img.shields.io/pypi/v/sweepai">\n<a href="https://pepy.tech/project/sweepai">\n    <img src="https://static.pepy.tech/badge/sweepai/month" />\n</a>\n<a href="https://github.com/sweepai/sweep">\n    <img src="https://img.shields.io/github/stars/sweepai/sweep" />\n</a>\n<a href="https://twitter.com/sweep__ai">\n    <img src="https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2Fsweep__ai" />\n</a>\n</p>\n\n<b>Sweep</b> is an AI junior developer that transforms bug reports & feature requests into code changes.\n\nDescribe bugs, small features, and refactors like you would to a junior developer, and Sweep:\n1. 🔍 reads your codebase\n2. 📝 plans the changes\n3. ⚡**writes a pull request with code**⚡\n\nSee highlights at https://docs.sweep.dev/examples.\n\n[Demo](https://github.com/sweepai/sweep/assets/44910023/365ec29f-7317-40a7-9b5e-0af02f2b0e47)\n\n## 🌠 Features\n* 🔧 Turns issues directly into pull requests (without an IDE)\n* 👀 Addresses developer replies & comments on its PRs\n* 🕵️\u200d♂️ Uses embedding-based code search, with popularity reranking for repository-level code understanding ([🔍 Rebuilding our Search Engine in a Day](https://docs.sweep.dev/blogs/building-code-search))\n* 🎊 New: Fixes PRs based on GitHub Actions feedback\n* 🎊 New: Sweep Chat, a local interface for Sweep (see below)\n* 🎊 New: Enhanced file handling with streaming logic in modify_file, allowing for larger files to be processed.\n\n## 🚀 Getting Started\n\n### ✨ Sweep Github App\nSetting up Sweep is as simple as adding the GitHub bot to a repo, then creating an issue for the bot to address. Here are the steps to get started:\n\n1. Add the [Sweep GitHub app](https://github.com/apps/sweep-ai) to your desired repos\n2. Read about [recipes](docs/Recipes.md) for best use cases.\n2. Create a new issue in your repo. The issue should describe the problem or feature you want Sweep to address. For example, you could write "Sweep: In sweepai/app/ui.py use an os-agnostic temp directory"\n3. Respond with a message like "Sweep: use a different package instead" to have Sweep retry the issue or pull request. You can also comment on the code for minor changes! Remember to put the "Sweep:" prefix.\n   - 💡 Hint: commenting "revert" reverts all edits in a file.\n\nWe support all languages GPT4 supports, including Python, Typescript, Rust, Go, Java, C# and C++.\n\n### 🗨️ Sweep Chat\nSweep Chat allows you to interact with Sweep and GitHub locally. You can collaborate on the plan with Sweep, and then have it create the pull request for you. Here\'s how to use Sweep Chat:\n\n**Prerequisites:** Install [Sweep GitHub app](https://github.com/apps/sweep-ai) to your repository\n\n1. Run `pip3 install sweepai && sweep`. Note that you need **python 3.10+.**\n    - Alternatively run `pip3 install --force-reinstall sweepai && sweep` if the previous command fails.\n    - This runs GitHub authentication in your browser.\n\n2. Copy the 🔵 blue 8-digit code from your terminal into the page. You should only need to do the authentication once.  \n    - Wait a few seconds and Sweep Chat will start. \n\n3. Choose a repository from the dropdown at the top (the Github app must be installed to this repository).\n    - ⚡ Start chatting with Sweep Chat! ⚡\n\n\n![Screenshot_20230711_015033](https://github.com/sweepai/sweep/assets/26889185/ed9f05d8-ef86-4f2a-9bca-acdfa24990ac)\n\nTips:\n* 🔍 Relevant searched files will show up on the right. \n* 🔘 Sweep Chat creates PRs when the "Create PR" button is clicked. \n* 💡 You can force dark mode by going to http://127.0.0.1:7861/?__theme=dark.\n\n#### From Source\nIf you want the nightly build and or if the latest build has issues.\n\n1. `git clone https://github.com/sweepai/sweep && poetry install`\n2. `python sweepai/app/cli.py`. Note that you need **python 3.10+**.\n\n## 💰 Pricing\n* We charge $120/month for 60 GPT4 tickets per month.\n* For unpaid users, we offer 5 free GPT4 tickets per month.\n* We also offer unlimited GPT3.5 tickets.\n\n## 🤝 Contributing\nContributions are welcome and greatly appreciated! For detailed guidelines on how to contribute, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.\nFor more detailed docs, see [🚀 Quickstart](https://docs.sweep.dev/).\n\n## 📘 Story\n\nWe were frustrated by small tickets, like simple bug fixes, annoying refactors, and small features. Each task required us to open our IDE to fix simple bugs. So we decided to leverage the capabilities of ChatGPT to address this directly in GitHub.\n\nUnlike existing AI solutions, this can solve entire tickets and can be parallelized + asynchronous: developers can spin up 10 tickets and Sweep will address them all at once.\n\n## 📚 The Stack\n- GPT-4 32k 0613 (default)\n- ActiveLoop DeepLake for Vector DB with MiniLM L12 as our embeddings model\n- Modal Labs for infra + deployment\n- Gradio for Sweep Chat\n\n## 🗺️ Roadmap\nSee [🗺️ Roadmap](https://docs.sweep.dev/roadmap)\n\n## ⭐ Star History\n\n[![Star History Chart](https://api.star-history.com/svg?repos=sweepai/sweep&type=Date)](https://star-history.com/#sweepai/sweep&Date)\n\nConsider starring us if you\'re using Sweep so more people hear about us!\n<h2 align="center">\n    Contributors\n</h2>\n<p align="center">\n    Thank you for your contribution!\n</p>\n<p align="center">\n    <a href="https://github.com/sweepai/sweep/graphs/contributors">\n      <img src="https://contrib.rocks/image?repo=sweepai/sweep" />\n    </a>\n</p>\n<p align="center">\n    and, of course, Sweep!\n</p>\n',
    'author': 'Kevin Lu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
