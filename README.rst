=======
sputils
=======


.. image:: https://img.shields.io/pypi/v/spotify-sputils.svg
        :target: https://pypi.python.org/pypi/spotify-sputils

.. image:: https://img.shields.io/travis/shanedabes/sputils.svg
        :target: https://travis-ci.org/shanedabes/sputils

.. image:: https://readthedocs.org/projects/sputils/badge/?version=latest
        :target: https://sputils.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/shanedabes/sputils/shield.svg
     :target: https://pyup.io/repos/github/shanedabes/sputils/
     :alt: Updates



A collection of spotify utilities, designed to be used in conjunction with other shell utilities.


* Free software: Apache Software License 2.0
* Documentation: https://sputils.readthedocs.io.


Features
--------

* Output spotify collection information:
    * Albums
    * Tracks
* Format output as:
    * json
    * lines
    * yaml

Install
-------

sputils can be installed using:

* pip_
* AUR_

.. _pip: https://pypi.org/project/spotify-sputils/
.. _AUR: https://aur.archlinux.org/packages/python-sputils/

**Note:** The spotipy package has a problem actually installing the new version, mentioned in this issue_. After installing sputils from pip, you will need to run:

    pip install git+https://github.com/plamere/spotipy.git --upgrade

.. _issue: https://github.com/plamere/spotipy/issues/211

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
