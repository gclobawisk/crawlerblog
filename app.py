from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from flask import Flask, request, render_template
import time
import mysql.connector
from mysql.connector import errorcode

db_connection = mysql.connector.connect(host='localhost', database='devnology', user='root', password='')
cursor = db_connection.cursor()


app = Flask(__name__)
@app.get('/')
def index():
    navegador = webdriver.Chrome()
    navegador.get("https://devgo.com.br")
    blog_id = 1
    while True:
        try:
            # Click no botão ler mais
            lermais = navegador.find_element(By.XPATH,
                                             '//*[@id="__next"]/div/div[3]/div/div[10]/button').click()
            time.sleep(3)

            links = navegador.find_elements(By.CLASS_NAME,
                                            'blog-article-card-title [href]')  # para obter o href do seletor <a> que fica a baixo

        except WebDriverException as erro:
            pass
            # print("Erro - exceção Webdriverexception: ", erro)

        for i in links:
            li_titulo = i.text
            li_url = i.get_property('href')


            sql = f"INSERT IGNORE INTO links (li_titulo, li_url, li_blog_id) VALUES ('{li_titulo}', '{li_url}', {1})"
            cursor.execute(sql)
            db_connection.commit()
            #print(i.text)
            #print(i.get_property('href'))
        break

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)




