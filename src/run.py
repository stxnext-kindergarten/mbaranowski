# -*- coding: utf-8 -*-
"""
Presence analyzer web app.
"""
import logging.config
import os.path

import presence_analyzer.views  # pylint: disable=unused-import
from presence_analyzer.main import app

INI_FILENAME = os.path.join(
    os.path.dirname(__file__), '..', 'runtime', 'debug.ini'
)


if __name__ == "__main__":
    logging.config.fileConfig(INI_FILENAME, disable_existing_loggers=False)
    app.run(host='0.0.0.0')
