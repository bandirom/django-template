Quick start!
============

This guide helps to install and run new projects.

Requirements
------------
* Docker with docker-compose

Usage
-----


# Clone the repository

.. code-block:: console

   $ git clone https://github.com/bandirom/django-template.git ./project_name

Before start let's set up superuser email and password (not username)

Open the project in your favorite IDE and edit :command:`docker/prod/env/.data.env` file.

Set up variables for superuser::

   SUPERUSER_EMAIL=example@email.com
   SUPERUSER_PASSWORD=secretpassword
   PROJECT_TITLE=MyProject

Run the local project with command:

.. code-block:: console

   $ docker-compose up -d --build

.. NOTE::

   You can run project without  :command:`-d (detach)` flag, if you don't need to run server everytime

.. NOTE::

   Project will bind 8000 port on your machine.
   If you wanna change it, you can do it in :command:`docker-compose.yml` in service :command:`web`

Let's check the logs of containers (Only if you use (-d) flag):

.. code-block:: console

   $ docker-compose logs -f

And visit `http://localhost:8000 <http://localhost:8000>`_.
