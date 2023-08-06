# buscador

Every time you want to update your package later on, upload a new version to github, create a new release as we just discussed, specify a new release tag and copy-paste the link to Source into the setup.py file (do not forget to also increment the version number).

https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

https://dillinger.io

New Version*
. Simply upload your new code to github, create a new release, then adapt the setup.py file (new download_url — according to your new release tag, new version), then run the setup.py and the twin command again (navigate to your folder first!)

- python setup.py sdist
- twine upload dist/*
