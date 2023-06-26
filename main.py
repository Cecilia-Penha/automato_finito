from tabulate import tabulate
#construcao de um automato para uma gramatica de soma de inteiros
#simbolos = 0,+,= (0 representa um numero de 0-9)
# ler
transicoes = {}

with open('entrada.txt', 'r') as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue
        
        estado, producoes = linha.split('::=')#pega estados
        producoes = producoes.split('|')#pega simbolos
        
        for producao in producoes:
            producao = producao.strip()
            if '<' not in producao:
                continue
            
            simbolo, prox_estados = producao.split('<')
            prox_estados = prox_estados.strip('>').split(',')
            
            for prox_estado in prox_estados:
                transicoes.setdefault((estado, simbolo), []).append(prox_estado)

# mostra transicoes
"""
for transicao, prox_estados in transicoes.items():
    estado_atual, simbolo = transicao
    for prox_estado in prox_estados:
        print(estado_atual, simbolo, prox_estado)
"""
#determinizar

# checa estado composto
def estado_composto(estado):
    return len(estado) > 1

def determinizar(transicoes):
    novas_transicoes = {}

    for estado, simbolo in transicoes.keys():
        proximos_estados = transicoes[(estado, simbolo)]#pega transicoes de cada estado
        
        if estado_composto(estado):
            novo_estado = ''.join(sorted(set(estado)))  #cria lista de estados compostos
            
            if novo_estado not in novas_transicoes:
                novas_transicoes[novo_estado] = {}
            
            for prox_estado in proximos_estados:
                if estado_composto(prox_estado):
                    novos_prox_estados = transicoes.get((prox_estado, '&'), [])#pega transicoes vazias
                    for prox_simbolo, prox_prox_estados in novos_prox_estados.items():
                        novas_transicoes[novo_estado].setdefault(prox_simbolo, []).extend(prox_prox_estados)
                else:
                    novas_transicoes[novo_estado].setdefault(simbolo, []).append(prox_estado)

    return novas_transicoes
#passar como tabela
def exibir_tabela(transicoes):
    simbolos = set()
    for estado, transicao in transicoes.items():
        simbolos.update(transicao.keys())
    headers = ['Estado'] + list(simbolos)
    table = []
    
    for estado, transicao in transicoes.items():
        row = [estado]
        for simbolo in simbolos:
            if simbolo in transicao:
                proximos_estados = transicao[simbolo]
                row.append(','.join(proximos_estados))
            else:
                row.append('')
        table.append(row)
    
    print(tabulate(table, headers, tablefmt='grid'))

transicoes_det = determinizar(transicoes)
exibir_tabela(transicoes_det)
#ler simbolos
def ler():
    try:
        with open('simbolos.txt','r')as file:
            automato = file.read().splitlines()
    except:
        print('erro na leitura')
    return automato    
automato = ler()
#definicao transicoes
def fita():
    estado_atual = 'S'#entrada S 
    i = 0
    estado = list()
    sim = list()
    while i < len(automato):
        simbolo = automato[i]                                                   
        if estado_atual == 'S':#transicoes S
            if simbolo.isdigit():
                estado_atual = 'A'
            else:
                estado_atual = 'X'
            i+=1
        elif estado_atual == 'A':#transicoes A
            if simbolo.isdigit():
                estado_atual = 'A'
            elif simbolo == '+':
                estado_atual = 'B'
            else:
                estado_atual = 'X'
            i+=1
        elif estado_atual == 'B':#transicoes B
            if simbolo.isdigit():
                estado_atual = 'BC'
            else:
                estado_atual = 'X'
            i+=1
        elif estado_atual == 'C':#transicoes C
            if simbolo == '=':
                estado_atual = 'D'
            else:
                estado_atual = 'X'
            i+=1
        elif estado_atual == 'D':#transicoes D
                if simbolo.isdigit():
                    estado_atual = 'DE'
                else:
                    estado_atual = 'X'
        elif estado_atual == 'BC':#transicoes BC
            if i+1 < len(automato):
                if simbolo in '=':
                    estado_atual = 'D'
                elif simbolo.isdigit():
                    estado_atual = 'BC'
                else:
                    estado_atual = 'X'
            else:
                estado_atual = 'X'
            i+=1
        elif estado_atual == 'DE':#transicoes *DE
            if i+1 < len(automato):
                if simbolo.isdigit():
                    estado_atual = 'DE'
                else:
                    estado_atual = 'X'
            else:
                estado_atual = '*E'
            i+=1
        elif estado_atual == '*E':
            break
        elif estado_atual == 'X':
            break
        estado.append(estado_atual)
        sim.append(simbolo)
    print("FITA:",estado,sim)
    return estado_atual,simbolo
fita()



