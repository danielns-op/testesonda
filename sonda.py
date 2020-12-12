from flask import Flask, abort
import json

app = Flask(__name__)

# Carrega a posição da sonda de um arquivo JSON.
with open('posicao_sonda.json', 'r') as carrega_posicao:
    sonda = json.load(carrega_posicao)
carrega_posicao.close()

# Limpa o arquivo de log.
limpa_arquivo = open('detalhes_movimento.log', 'w')
limpa_arquivo.close()


@app.route('/')
def index():
    html = ["<ul><title>Sonda</title>"
            "<li><a href='/retorno'>Retorna posição</a></li>"
            "<li><a href='/atual'>Posição atual</a></li></ul>"]
    return '\n'.join(html)


@app.route('/retorno')
def posicao_inicial():
    pos_inicio = {'x': 0, 'y': 0, 'Direcao': 'D'}
    with open('posicao_sonda.json', 'w') as retomar_posicao:
        json.dump(pos_inicio, retomar_posicao)
    retomar_posicao.close()
    retorno = ["<ul><span>Sonda retomada para a posição inicial.</span><br><br><a href='/'>HOME</a></ul>"]
    return '\n'.join(retorno)


@app.route('/atual')
def posicao_atual():
    with open('posicao_sonda.json', 'r') as ver_posicao:
        posicao = json.load(ver_posicao)
    ver_posicao.close()
    pos_atual = [f"<ul><span>Posição atual da Sonda: {posicao}</span><br><br><a href='/'>HOME</a></ul>"]
    return 'n'.join(pos_atual)


@app.route('/move/<valor>/')
def movimentar(valor):
    log = open('detalhes_movimento.log', 'a')
    move = 'x'  # Caso (0, 0) movimenta no eixo X.
    movimento = valor.strip().upper().split(',')
    for acao in movimento:
        if acao == 'GE' and sonda['Direcao'] == 'D':
            sonda['Direcao'] = 'C'
            log.write('Girou para a esquerda e ficou com a face para Cima.\n')
            move = 'y'
        elif acao == 'GE' and sonda['Direcao'] == 'C':
            sonda['Direcao'] = 'E'
            log.write('Girou para a esquerda e ficou com a face para Esquerda.\n')
            move = 'x'
        elif acao == 'GE' and sonda['Direcao'] == 'E':
            sonda['Direcao'] = 'B'
            log.write('Girou para a esquerda e ficou com a face para Baixo.\n')
            move = 'y'
        elif acao == 'GE' and sonda['Direcao'] == 'B':
            sonda['Direcao'] = 'D'
            log.write('Girou para a esquerda e ficou com a face para Direita.\n')
            move = 'x'
        if acao == 'GD' and sonda['Direcao'] == 'D':
            sonda['Direcao'] = 'B'
            log.write('Girou para a direita e ficou com a face para Baixo.\n')
            move = 'y'
        elif acao == 'GD' and sonda['Direcao'] == 'B':
            sonda['Direcao'] = 'E'
            log.write('Girou para a direita e ficou com a face para Esquerda.\n')
            move = 'x'
        elif acao == 'GD' and sonda['Direcao'] == 'E':
            sonda['Direcao'] = 'C'
            log.write('Girou para a direita e ficou com a face para Cima.\n')
            move = 'y'
        elif acao == 'GD' and sonda['Direcao'] == 'C':
            sonda['Direcao'] = 'D'
            log.write('Girou para a direita e ficou com a face para Direita.\n')
            move = 'x'
        if acao == 'M' and sonda['Direcao'] == 'C':
            sonda[move] += 1
            log.write('Moveu uma casa no eixo y.\n')
        elif acao == 'M' and sonda['Direcao'] == 'D':
            sonda[move] += 1
            log.write('Moveu uma casa no eixo x.\n')
        elif acao == 'M' and sonda['Direcao'] == 'E':
            sonda[move] -= 1
            log.write('Moveu uma casa no eixo x.\n')
        elif acao == 'M' and sonda['Direcao'] == 'B':
            sonda[move] -= 1
            log.write('Moveu uma casa no eixo y.\n')
    log.close()
    if sonda['x'] > 4 or sonda['x'] < 0 or sonda['y'] > 4 or sonda['y'] < 0:
        limpa_log = open('detalhes_movimento.log', 'w')
        limpa_log.close()
        return abort(409, f"Um movimento inválido foi detectado.")
    else:
        with open('posicao_sonda.json', 'w') as grava_posicao:
            json.dump(sonda, grava_posicao)
        grava_posicao.close()
        ler_log = open('detalhes_movimento.log', 'r')
        log_movimento = ler_log.read()
        return f'Log movimentos:\n{log_movimento}\n\nPosição final: {sonda}'


app.run(use_reloader=True)
