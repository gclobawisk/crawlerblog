from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from flask import Flask, request, render_template
import time

app = Flask(__name__)
@app.route('/')
def hello():
    navegador = webdriver.Chrome()
    navegador.get("https://devgo.com.br")
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
            print(i.text)
            print(i.get_property('href'))
        break

    return render_template('index.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)




