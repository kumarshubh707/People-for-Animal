from app import app
from flask import redirect, url_for, request, render_template
from .queries import *

@app.route('/')
def fun():
    pass