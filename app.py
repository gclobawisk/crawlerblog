from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from flask import Flask, request, render_template, redirect, jsonify
import time
import mysql.connector
from mysql.connector import errorcode

# CONEXAO AO BANCO DE DADOS
db_connection = mysql.connector.connect(host='devnology99.mysql.dbaas.com.br', database='devnology99',
                                            user='devnology99', password='Devnology99@')
cursor = db_connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM links")
links = cursor.fetchall()


# CRIANDO O APP
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/')
def index():
    return render_template('index.html')

# CRAWLER
@app.route('/crawler')
def crawler():
    db_connection = mysql.connector.connect(host='devnology99.mysql.dbaas.com.br', database='devnology99',
                                            user='devnology99', password='Devnology99@')
    cursor = db_connection.cursor()

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

    return render_template('sucesso.html')

# Consultar todos os links
@app.route('/links')
def getLinks():
    return jsonify(links)


# Consultar link por id'
@app.route('/links/<int:id>', methods=['GET'])
def obter_link_por_id(id):
    for link in links:
        if link.get('li_id') == id:
            return jsonify(link)

    if TypeError:
        return ('ID inválido')


#EDITAR
@app.route('/links/<int:id>', methods=['PUT'])
def editar_link(id):
    link_alterado = request.get_json()
    for i,link in enumerate(links):
        if link.get("li_id") == id:
            links[i].update(link_alterado)
            return jsonify(links[i])
    if TypeError:
        return ('ID inválido')

@app.route('/links', methods=['POST'])
def incluir_link():
    novo_link = request.get_json()
    links.append(novo_link)
    return jsonify(links)

@app.route('/links/<int:id>', methods=['DELETE'])
def excluir_link(id):
    for i, link in enumerate(links):
        if link.get("li_id") == id:
            del links[i]
            return jsonify(links)
    if TypeError:
        return ('ID inválido')



if __name__ == '__main__':
    app.run(debug=True)

