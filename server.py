# -*- coding: utf-8 -*-
import dash
from dash import Dash
from flask import Flask, request
import os

server = Flask(__name__, static_url_path='/static', static_folder='./static')
server.secret_key = os.environ.get('secret_key', 'secret')
app = Dash(__name__, server=server, url_base_pathname='/', csrf_protect=False)

app.config.supress_callback_exceptions = True