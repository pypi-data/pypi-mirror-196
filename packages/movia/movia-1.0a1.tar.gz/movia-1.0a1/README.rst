.. rst syntax: https://deusyss.developpez.com/tutoriels/Python/SphinxDoc/
.. icons: https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html or https://www.pythonguis.com/faq/built-in-qicons-pyqt/
.. pyqtdoc: https://www.riverbankcomputing.com/static/Docs/PyQt6/


.. image:: https://github.com/pytest-dev/pytest/workflows/test/badge.svg
    :target: https://github.com/pytest-dev/pytest/actions?query=workflow%3Atest

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

**************************************
movia, a light video editing software!
**************************************

Decsription
-----------

This software proposes a graphic interface powered by pyqt6 (run ``movia``).
The kernel is written in python and is easily integrated in other projects (module ``movia.core``).

This software is **light**, **fast** and **highly configurable** for the following reasons:

1. Based on ffmpeg, this software supports an incredible number of formats and codecs.
2. Thanks to operations on the assembly graph, it is able to perform nbr_opti optimization operations.
3. nbr_tests unit tests ensure an excelent kernel reliability.
4. Unlike other software that offers a timeline, this one allows you to edit an editing graph. This representation is more general and thus allows a greater flexibility.
5. A compiled version without graphical interface allows to allocate all the resources of the computer to the export.
6. This software generates at the time of the export a python code which can be edited. This offers an infinite number of possibilities!

Installation
------------

Dependencies
^^^^^^^^^^^^

* `ffmpeg5 <https://ubuntuhandbook.org/index.php/2022/02/install-ffmpeg-5-0-ubuntu/>`_

.. code:: bash

    sudo add-apt-repository ppa:savoury1/ffmpeg4
    sudo add-apt-repository ppa:savoury1/ffmpeg5
    sudo apt update
    sudo apt full-upgrade
    sudo apt install ffmpeg

* `pygraphviz <https://pygraphviz.github.io/documentation/stable/install.html>`_

.. code:: bash

    sudo apt install graphviz graphviz-dev pygraphviz

Depos
^^^^^

.. code:: bash

    git clone https://framagit.org/robinechuca/movia.git
    cd movia/
    python -m pip install -e ./

Run
^^^

.. code:: bash

    movia


What's new ?
------------

Nothing new for the moment.
