from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from flask import Flask, request, render_template
import time
import mysql.connector
from mysql.connector import errorcode



app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True)
