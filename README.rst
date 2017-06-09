=====================
NorthEuraLex: website
=====================

In this repo lives the web interface to the NorthEuraLex database. It is a
`clld`_ app.


setup
=====

::
    
    # clone this repository
    git clone https://github.com/evolaemp/northeuralex_website
    cd northeuralex_website

    # you do not need to create a virtual env if you know what you are doing
    # note that this is a python 3 project
    pyvenv path/to/my/venv
    source path/to/my/venv/bin/activate

    # install the dependencies (there are quite a few of these)
    # it is important to use the versions specified in the requirements file
    pip install -r requirements.txt

    # clld wants its projects to be python packages, so you have to register
    # the northeuralex package with the virtual env
    python setup.py develop

    # in a development setup the database is an sqlite3 instance living in meta
    mkdir meta
    python northeuralex/scripts/initializedb.py development.ini --module northeuralex path/to/northeuralex_data path/to/lang_data

    # check the unit tests
    python setup.py test

    # run the development server at localhost:6543
    pserve --reload development.ini


.. _`clld`: http://clld.org/
