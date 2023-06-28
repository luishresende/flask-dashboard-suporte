from datetime import datetime, timedelta
import json
import requests
import base64


def payload(grid, query):
    return {
        'qtype': 'su_oss_chamado.id_assunto',
        'query': f'{str(query)}',
        'oper': '=',
        'page': '1',
        'rp': '500',
        'sortname': 'su_oss_chamado.id',
        'sortorder': 'asc',
        'grid_param': grid
    }


def em_aberto(url_kdm, url_tele, headers_kdm, headers_tele):
    prazo_vencido = 0
    assumidos = 0
    critico_assumido = 0
    critico_vencido = 0

    grid = '[{\"TB\":\"su_oss_chamado.status\", \"OP\" : \"!=\", \"P\" : \"F\"}]'

    em_aberto_kdm = requests.post(url_kdm, data=json.dumps(payload(grid, 135)), headers=headers_kdm).json()
    em_aberto_tele = requests.post(url_tele, data=json.dumps(payload(grid, 18)), headers=headers_tele).json()
    em_aberto_critico_kdm = requests.post(url_kdm, data=json.dumps(payload(grid, 295)), headers=headers_kdm).json()
    em_aberto_critico_tele = requests.post(url_tele, data=json.dumps(payload(grid, 156)), headers=headers_tele).json()

    formato_data = '%Y-%m-%d %H:%M:%S'
    data_atual = datetime.strptime(str(datetime.now())[:19], formato_data)

    total = int(em_aberto_kdm['total']) + int(em_aberto_tele['total']) + int(em_aberto_critico_kdm['total']) + int(em_aberto_critico_tele['total'])
    criticos = int(em_aberto_critico_kdm['total']) + int(em_aberto_critico_tele['total'])

    try:
        em_aberto_kdm = em_aberto_kdm['registros']
    except KeyError as error:
        pass
    else:
        for registro in em_aberto_kdm:
            data_abertura = datetime.strptime(registro['data_abertura'], formato_data)
            tempo_aberto = data_atual - data_abertura
            if tempo_aberto.days >= 2 and registro['status'] != 'AS':
                prazo_vencido += 1
            if registro['status'] == 'AS':
                assumidos += 1


    try:
        em_aberto_tele = em_aberto_tele['registros']
    except KeyError as error:
        pass
    else:
        for registro in em_aberto_tele:
            data_abertura = datetime.strptime(registro['data_abertura'], formato_data)
            tempo_aberto = data_atual - data_abertura
            if tempo_aberto.days >= 2 and registro['status'] != 'AS':
                prazo_vencido += 1
            if registro['status'] == 'AS':
                assumidos += 1


    try:
        em_aberto_critico_kdm = em_aberto_critico_kdm['registros']
    except KeyError as error:
        pass
    else:
        for registro in em_aberto_critico_kdm:
            data_abertura = datetime.strptime(registro['data_abertura'], formato_data)
            tempo_aberto = data_atual - data_abertura
            if tempo_aberto.days >= 2 and registro['status'] != 'AS':
                prazo_vencido += 1
                critico_vencido += 1
            if registro['status'] == 'AS':
                assumidos += 1
                critico_assumido += 1


    try:
        em_aberto_critico_tele = em_aberto_critico_tele['registros']
    except KeyError as error:
        pass
    else:
        for registro in em_aberto_critico_tele:
            data_abertura = datetime.strptime(registro['data_abertura'], formato_data)
            tempo_aberto = data_atual - data_abertura
            if tempo_aberto.days >= 2 and registro['status'] != 'AS':
                prazo_vencido += 1
                critico_vencido += 1
            if registro['status'] == 'AS':
                assumidos += 1
                critico_assumido += 1

    if criticos > 0:
        cor_critico = 'red'
    else:
        cor_critico = '#0071B9'

    if critico_vencido > 0:
        cor_vencido = 'red'
    else:
        cor_vencido = '#0071B9'

    if critico_assumido > 0:
        cor_assumido = 'red'
        if critico_assumido == criticos:
            cor_critico = '#0071B9'
    else:
        cor_assumido = '#0071B9'

    return [total, prazo_vencido, assumidos, criticos, [cor_critico, cor_vencido, cor_assumido]]


def finalizados(url_kdm, url_tele, headers_kdm, headers_tele):
    grid = f'[{{\"TB\":\"su_oss_chamado.status\", \"OP\" : \"=\", \"P\" : \"F\"}}, {{\"TB\":\"su_oss_chamado.data_fechamento\", \"OP\" : \">=\", \"P\" : \"{str(datetime.now().date())}\"}}]'
    finalizados_kdm = requests.post(url_kdm, data=json.dumps(payload(grid, 135)), headers=headers_kdm).json()
    finalizados_tele = requests.post(url_tele, data=json.dumps(payload(grid, 18)), headers=headers_tele).json()
    finalizados_critico_kdm = requests.post(url_kdm, data=json.dumps(payload(grid, 295)), headers=headers_kdm).json()
    finalizados_critico_tele = requests.post(url_tele, data=json.dumps(payload(grid, 156)), headers=headers_tele).json()
    total = int(finalizados_kdm['total']) + int(finalizados_tele['total']) + int(finalizados_critico_kdm['total']) + int(finalizados_critico_tele['total'])

    return [total]


def sem_acesso(headers_kdm, headers_tele):
    url_kdm = "https://kdminfo.com.br/webservice/v1/radusuarios"
    url_tele = "https://shtelecom.net.br/webservice/v1/radusuarios"
    payloadSA = {
        'qtype': 'radusuarios.ativo',
        'query': 'S',
        'oper': '=',
        'page': '1',
        'rp': '500',
        'sortname': 'radusuarios.id_cliente',
        'sortorder': 'asc',
        'grid_param': '[{\"TB\":\"radusuarios.online\", \"OP\" : \"=\", \"P\" : \"N\"}]'
    }
    sem_acesso_kdm = requests.post(url_kdm, data=json.dumps(payloadSA), headers=headers_kdm).json()
    sem_acesso_tele = requests.post(url_tele, data=json.dumps(payloadSA), headers=headers_tele).json()
    return [int(sem_acesso_kdm['total']), int(sem_acesso_tele['total'])]


def obter_dados():
    url_kdm = "https://kdminfo.com.br/webservice/v1/su_oss_chamado"
    url_tele = "https://shtelecom.net.br/webservice/v1/su_oss_chamado"
    token_kdm = "token"
    token_tele = "token"

    headers_kdm = {
        'ixcsoft': 'listar',
        'Authorization': 'Basic {}'.format(base64.b64encode(token_kdm).decode('utf-8')),
        'Content-Type': 'application/json'
    }

    headers_tele = {
        'ixcsoft': 'listar',
        'Authorization': 'Basic {}'.format(base64.b64encode(token_tele).decode('utf-8')),
        'Content-Type': 'application/json'
    }

    return {'finalizados': finalizados(url_kdm, url_tele, headers_kdm, headers_tele), 'em_aberto': em_aberto(url_kdm, url_tele, headers_kdm, headers_tele), 'sem_acesso': sem_acesso(headers_kdm, headers_tele)}


def opa():
    headers = {
        'Authorization': f'Bearer token',
        'Content-Type': 'application/json'
    }
    filter = {
        'protocolo': f"OPA{datetime.now().year}"
    }
    options = {
        'limit': '150000'
    }
    payload = {'options': options}
    print(f'OPA{datetime.now().year}')
    result = requests.get('url', data=json.dumps(payload), headers=headers).json()
    print(result)