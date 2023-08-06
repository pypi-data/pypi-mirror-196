"""
Description
===========

Usage
=====

.. code-block:: python

  #!/usr/bin/env python3

  from flask import Flask
  from flask_gordon.ext import CeleryExt

  flask = Flask(__name__)
  celery = CeleryExt(flask)


Classes
=======

.. autoclass:: Celery
   :members: init_app

"""
import importlib
import os
import typing as t

from boltons.fileutils import iter_find_files

try:
    from celery import Celery, Task

    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False


class CeleryExt:
    def __init__(self):
        if not HAS_CELERY:
            raise NotImplementedError("CeleryExt requires celery[redis] package")

    def init_app(
        self,
        app: "Flask",
    ):
        """
        Parameters
        ----------
        app: FlaskApp

            A Flask application.
        """

        # pylint: disable=abstract-method
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: t.Dict[str, t.Any]) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_app = Celery(app.name, task_cls=FlaskTask)
        for name in ["celery", "CELERY"]:
            if name in app.config:
                celery_app.config_from_object(app.config[name])
                break
        else:
            app.config.update(
                CELERY={
                    "broker_url": "redis://localhost:6379/0",
                    "result_backend": "redis://localhost:6379/0",
                },
            )
            celery_app.config_from_object(app.config["CELERY"])

        celery_app.set_default()
        app.extensions["celery"] = celery_app

        return celery_app

    @staticmethod
    def load(module: str, path: str):
        if not os.path.isdir(path):
            path = os.path.dirname(path)

        # Load all files in "tasks" folder
        path = os.path.join(path, "tasks")
        files = iter_find_files(path, "*.py")

        for file in files:
            name, _ = os.path.splitext(os.path.basename(file))
            print(name)
            importlib.import_module(f"{module}.tasks.{name}")
