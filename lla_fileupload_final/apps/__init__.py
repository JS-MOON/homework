from flask import Flask
import os

app = Flask('apps')
app.config.from_object('apps.settings.Production')

import views