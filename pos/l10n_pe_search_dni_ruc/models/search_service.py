# -*- encoding: utf-8 -*-
import requests

STATE = [('ACTIVO', 'ACTIVO'),
		 ('BAJA DE OFICIO', 'BAJA DE OFICIO'),
		 ('BAJA DEFINITIVA', 'BAJA DEFINITIVA'),
		 ('BAJA PROVISIONAL', 'BAJA PROVISIONAL'),
		 ('SUSPENSION TEMPORAL', 'BAJA PROVISIONAL'),
		 ('INHABILITADO-VENT.UN', 'INHABILITADO-VENT.UN'),
		 ('BAJA MULT.INSCR. Y O', 'BAJA MULT.INSCR. Y O'),
		 ('PENDIENTE DE INI. DE', 'PENDIENTE DE INI. DE'),
		 ('OTROS OBLIGADOS', 'OTROS OBLIGADOS'),
		 ('NUM. INTERNO IDENTIF', 'NUM. INTERNO IDENTIF'),
		 ('ANUL.PROVI.-ACTO ILI', 'ANUL.PROVI.-ACTO ILI'),
		 ('ANULACION - ACTO ILI', 'ANULACION - ACTO ILI'),
		 ('BAJA PROV. POR OFICI', 'BAJA PROV. POR OFICI'),
		 ('ANULACION - ERROR SU', 'ANULACION - ERROR SU')]

CONDITION = [('HABIDO', 'HABIDO'),
			 ('NO HABIDO', 'NO HABIDO'),
			 ('NO HALLADO', 'NO HALLADO'),
			 ('PENDIENTE', 'PENDIENTE'),
			 ('NO HALLADO SE MUDO D', 'NO HALLADO SE MUDO D'),
			 ('NO HALLADO NO EXISTE', 'NO HALLADO NO EXISTE'),
			 ('NO HALLADO FALLECIO', 'NO HALLADO FALLECIO'),
			 ('-', 'NO HABIDO'),
			 ('NO HALLADO OTROS MOT', 'NO HALLADO OTROS MOT'),
			 ('NO APLICABLE', 'NO APLICABLE'),
			 ('NO HALLADO NRO.PUERT', 'NO HALLADO NRO.PUERT'),
			 ('NO HALLADO CERRADO', 'NO HALLADO CERRADO'),
			 ('POR VERIFICAR', 'POR VERIFICAR'),
			 ('NO HALLADO DESTINATA', 'NO HALLADO DESTINATA'),
			 ('NO HALLADO RECHAZADO', 'NO HALLADO RECHAZADO')]

def fetch_dni_from_apiperu(token, dni):
    endpoint = f"https://apiperu.dev/api/dni/{dni}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code != 200:
            return ""
        
        data = response.json().get('data', {})
        return data.get('nombre_completo', "")
        
    except Exception:
        return ""

def fetch_dni_from_apimigo(token, dni):
    endpoint = "https://api.migo.pe/api/v1/dni/"
    request_data = {
        'dni': dni,
        'token': token
    }
    try:
        response = requests.post(url=endpoint, data=request_data)
        response.raise_for_status()
        
        data = response.json()
        return data.get('nombre', "")
    
    except requests.exceptions.RequestException:
        return ""
    
    except ValueError:
        return ""
    
    except Exception:
        return ""

def fetch_dni_from_jsonpe(token, dni):
    try:
        endpoint = f"https://api.json-pe.com/dni/{dni}?apikey={token}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            return {'error': True, 'message': 'Error retrieving DNI data'}

        data = response.json().get('body', {})
        full_name = f"{data.get('apePaterno', '')} {data.get('apeMaterno', '')}, {data.get('preNombres', '')}".strip()

        return full_name

    except Exception as e:
        return {'error': True, 'message': str(e)}

def fetch_ruc_from_apiperu(token, ruc):
    try:
        endpoint = "https://apiperu.dev/api/ruc/%s" % ruc
        headers = {
            "Authorization": "Bearer %s" % token,
            "Content-Type": "application/json",
        }
        taxpayer_data = requests.get(endpoint, data={}, headers=headers)
        
        if taxpayer_data.status_code == 200:
            taxpayer_data = taxpayer_data.json()
            ubigeo = taxpayer_data['data']['ubigeo'][2]
            address = taxpayer_data['data']['direccion_completa'] if 'direccion_completa' in taxpayer_data['data'] else ''
            if not address:
                address = ''
            if not ubigeo:
                ubigeo = '-'

            data = {
                'error': False,
                'message': 'ok',
                'condition': taxpayer_data['data']['condicion'],
                'status': taxpayer_data['data']['estado'],
                'ubigeo': ubigeo if ubigeo != "-" else "150101",
                'address': address.split(',')[0],
                'company_name': taxpayer_data['data']['nombre_o_razon_social'],
                'ruc': taxpayer_data['data']['ruc'],
                'departamento': taxpayer_data['data']['departamento'],
                'provincia': taxpayer_data['data']['provincia'],
                'distrito': taxpayer_data['data']['distrito'],
            }
            return data
        else:
            return {'error': True, 'message': 'Error retrieving data'}
    except Exception as e:
        return {'error': True, 'message': str(e)}

def fetch_ruc_from_apimigo(token, ruc):
    endpoint = "https://api.migo.pe/api/v1/ruc/"
    request_data = {
        'ruc': ruc,
        'token': token
    }
    try:
        response = requests.post(url=endpoint, data=request_data)
        response.raise_for_status()

        taxpayer_data = response.json()
        
        data = {
            'error': False,
            'message': 'ok',
            'condition': taxpayer_data .get('condicion_de_domicilio', ''),
            'status': taxpayer_data .get('estado_del_contribuyente', ''),
            'ubigeo': taxpayer_data .get('ubigeo', "150101"),
            'distrito':  taxpayer_data.get('distrito'),
            'provincia':  taxpayer_data.get('provincia'),
            'departamento': taxpayer_data.get('departamento'),
            'address': taxpayer_data.get('direccion_simple', ''),
            'company_name': taxpayer_data.get('nombre_o_razon_social', ''),
            'ruc': taxpayer_data.get('ruc', '')
        }

        good_contributor_data  = check_good_contributor(token, ruc)
        data['buen_contribuyente'] = good_contributor_data .get('buen_contribuyente', False)
        data['from_date'] = good_contributor_data  .get('a_partir_del', "")
        data['resolution'] = good_contributor_data .get('resolucion', "")

        return data

    except requests.exceptions.RequestException:
        return {'error': True, 'message': 'Failed to load data'}

    except ValueError:
        return {'error': True, 'message': 'Invalid JSON response'}

    except Exception:
        return {'error': True, 'message': 'Could not retrieve a valid response'}

def fetch_ruc_from_jsonpe(token, ruc):
    try:
        endpoint = f"https://api.json-pe.com/ruc/{ruc}?apikey={token}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            return {'error': True, 'message': 'Error retrieving RUC data'}

        data = response.json().get('body', {})
        taxpayer_data = data.get('datosContribuyente', {})

        return {
            'error': False,
            'message': 'ok',
            'ruc': data.get('numeroRUC', ruc),
            'company_name': taxpayer_data.get('desRazonSocial', ''),
            'trade_name': taxpayer_data.get('desNomApe', ''),
            'address': taxpayer_data.get('desDireccion', ''),
            'condition': taxpayer_data.get('codDomHabido', ''),
            'status': taxpayer_data.get('codEstado', ''),
            'ubigeo': taxpayer_data.get('ubigeo', {}).get('codUbigeo', ''),
            'distrito': taxpayer_data.get('ubigeo', {}).get('desDistrito', ''),
            'provincia': taxpayer_data.get('ubigeo', {}).get('desProvincia', ''),
            'departamento': taxpayer_data.get('ubigeo', {}).get('desDepartamento', '')
        }

    except Exception as e:
        return {'error': True, 'message': str(e)}

def check_good_contributor(token, ruc):
    endpoint = "https://api.migo.pe/api/v1/ruc/buenos-contribuyentes"
    request_data  = {
        'ruc': ruc,
        'token': token
    }
    response_data  = {
        'buen_contribuyente': False,
    }
    try:
        response = requests.post(url=endpoint, data= request_data)
        response.raise_for_status()
        
        response_data  = response.json()
        response_data ['buen_contribuyente'] = True
        return response_data 

    except requests.exceptions.RequestException:
        return response_data 
