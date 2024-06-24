from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="gabriel",
    password="26486314",
    database="aula_13_10"
)
cursor = db.cursor()

@app.route('/')
def index():
    return redirect(url_for('funcionario'))

@app.route('/funcionario', methods=['GET', 'POST'])
def funcionario():
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        data_admissao = request.form['data_admissao']
        status_funcionario = 1 if 'status_funcionario' in request.form else 0
        cursor.execute("INSERT INTO funcionarios (primeiro_nome, sobrenome, data_admissao, status_funcionario) VALUES (%s, %s, %s, %s)",
                       (primeiro_nome, sobrenome, data_admissao, status_funcionario))
        db.commit()
        return redirect(url_for('funcionario'))
    return render_template('funcionario.html')

@app.route('/dados')
def dados():
    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()
    return render_template('dados.html', funcionarios=funcionarios)




@app.route('/funcionario/deletar/<int:id_funcionario>', methods=['POST'])
def deletar_funcionario(id_funcionario):
    cursor.execute("DELETE FROM funcionarios WHERE id = %s", (id_funcionario,))
    db.commit()
    return redirect(url_for('dados'))

@app.route('/funcionario/atualizar_formulario/<int:id_funcionario>', methods=['GET'])
def atualizar_formulario(id_funcionario):
    cursor.execute("SELECT * FROM funcionarios WHERE id = %s", (id_funcionario,))
    funcionario_para_atualizar = cursor.fetchone()
    cursor.execute("SELECT * FROM funcionarios")  
    funcionarios = cursor.fetchall()  
    return render_template('dados.html', funcionarios=funcionarios, funcionario_para_atualizar=funcionario_para_atualizar, id_funcionario=id_funcionario)

@app.route('/funcionario/atualizar/<int:id_funcionario>', methods=['POST'])
def atualizar_funcionario(id_funcionario):
    primeiro_nome = request.form['primeiro_nome']
    sobrenome = request.form['sobrenome']
    data_admissao = request.form['data_admissao']
    status_funcionario = 1 if 'status_funcionario' in request.form else 0
    cursor.execute("UPDATE funcionarios SET primeiro_nome=%s, sobrenome=%s, data_admissao=%s, status_funcionario=%s WHERE id=%s",
                   (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_funcionario))
    db.commit()
    return redirect(url_for('dados'))


if __name__ == '__main__':
    app.run()