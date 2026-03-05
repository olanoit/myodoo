# -*- coding: utf-8 -*-

import requests
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    dni = fields.Char(
        string='DNI',
        help='Documento Nacional de Identidad',
        index=True,
    )
    ruc = fields.Char(
        string='RUC',
        help='Registro Único de Contribuyente',
        index=True,
    )

    @api.constrains('dni')
    def _check_dni(self):
        """Validar formato del DNI (8 dígitos)"""
        for record in self:
            if record.dni and (not record.dni.isdigit() or len(record.dni) != 8):
                raise ValidationError(_('El DNI debe tener 8 dígitos numéricos.'))

    @api.constrains('ruc')
    def _check_ruc(self):
        """Validar formato del RUC (11 dígitos)"""
        for record in self:
            if record.ruc and (not record.ruc.isdigit() or len(record.ruc) != 11):
                raise ValidationError(_('El RUC debe tener 11 dígitos numéricos.'))

    def _get_json_pe_api_token(self):
        """Obtener el API token desde la configuración"""
        return self.env['ir.config_parameter'].sudo().get_param('json_pe.api_token', '')

    def _call_json_pe_api(self, endpoint, payload):
        """
        Llamar a la API de json.pe
        
        :param endpoint: 'dni' o 'ruc'
        :param payload: dict con 'dni' o 'ruc'
        :return: dict con la respuesta de la API
        :raises: UserError si hay error en la llamada
        """
        api_token = self._get_json_pe_api_token()
        
        if not api_token:
            raise UserError(_(
                'No se ha configurado el API Token de json.pe. '
                'Por favor, crea tu cuenta en app.json.pe, obtén tu token y configúralo en Configuración > Configuración General.'
            ))

        url = f'https://api.json.pe/api/{endpoint}'
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }

        try:
            _logger.info(f'Consultando API json.pe: {url} con payload: {payload}')
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('success', False):
                error_message = data.get('message', 'Error desconocido')
                raise UserError(_('Error en la API de json.pe: %s') % error_message)
            
            return data.get('data', {})
            
        except requests.exceptions.Timeout:
            raise UserError(_('Timeout al consultar la API de json.pe. Por favor, intenta nuevamente.'))
        except requests.exceptions.ConnectionError:
            raise UserError(_('Error de conexión con la API de json.pe. Verifica tu conexión a internet.'))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise UserError(_('Token de API inválido. Verifica la configuración del API Token.'))
            elif e.response.status_code == 429:
                raise UserError(_('Límite de consultas excedido. Por favor, intenta más tarde.'))
            else:
                raise UserError(_('Error HTTP %s al consultar la API de json.pe.') % e.response.status_code)
        except requests.exceptions.RequestException as e:
            _logger.error(f'Error al consultar API json.pe: {str(e)}')
            raise UserError(_('Error al consultar la API de json.pe: %s') % str(e))
        except Exception as e:
            _logger.error(f'Error inesperado al consultar API json.pe: {str(e)}')
            raise UserError(_('Error inesperado al consultar la API: %s') % str(e))

    def action_consultar_dni(self):
        """
        Consultar DNI desde la API de json.pe y autocompletar campos del partner
        """
        self.ensure_one()
        
        if not self.dni:
            raise UserError(_('Por favor, ingresa un DNI antes de consultar.'))
        
        # Validar formato del DNI
        if not self.dni.isdigit() or len(self.dni) != 8:
            raise UserError(_('El DNI debe tener 8 dígitos numéricos.'))
        
        # Llamar a la API
        payload = {'dni': self.dni}
        data = self._call_json_pe_api('dni', payload)
        
        # Actualizar campos del partner
        update_vals = {}
        
        if data.get('nombre_completo'):
            update_vals['name'] = data['nombre_completo']
        
        # Si hay dirección, actualizar street
        if data.get('direccion_completa'):
            update_vals['street'] = data['direccion_completa']
        elif data.get('direccion'):
            update_vals['street'] = data['direccion']
        
        # Actualizar campos si hay valores
        if update_vals:
            self.write(update_vals)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Consulta exitosa'),
                    'message': _('Los datos del DNI se han actualizado correctamente.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Consulta completada'),
                    'message': _('La consulta se realizó correctamente, pero no se encontraron datos adicionales para actualizar.'),
                    'type': 'info',
                    'sticky': False,
                }
            }

    def action_consultar_ruc(self):
        """
        Consultar RUC desde la API de json.pe y autocompletar campos del partner
        """
        self.ensure_one()
        
        if not self.ruc:
            raise UserError(_('Por favor, ingresa un RUC antes de consultar.'))
        
        # Validar formato del RUC
        if not self.ruc.isdigit() or len(self.ruc) != 11:
            raise UserError(_('El RUC debe tener 11 dígitos numéricos.'))
        
        # Llamar a la API
        payload = {'ruc': self.ruc}
        data = self._call_json_pe_api('ruc', payload)
        
        # Actualizar campos del partner
        update_vals = {}
        
        if data.get('nombre_o_razon_social'):
            update_vals['name'] = data['nombre_o_razon_social']
        
        # Actualizar VAT con el RUC
        if self.ruc:
            update_vals['vat'] = f'PE{self.ruc}'
        
        # Actualizar dirección
        if data.get('direccion_completa'):
            update_vals['street'] = data['direccion_completa']
        elif data.get('direccion'):
            update_vals['street'] = data['direccion']
        
        # Actualizar ciudad, estado y código postal si están disponibles
        if data.get('distrito'):
            update_vals['city'] = data['distrito']
        
        if data.get('provincia'):
            # En Odoo, el campo 'state_id' es una relación, pero podemos usar 'state' como texto
            # Si hay un estado definido en el sistema, se puede mapear
            pass
        
        if data.get('ubigeo_sunat'):
            update_vals['zip'] = data['ubigeo_sunat']
        
        # Actualizar campos si hay valores
        if update_vals:
            self.write(update_vals)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Consulta exitosa'),
                    'message': _('Los datos del RUC se han actualizado correctamente.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Consulta completada'),
                    'message': _('La consulta se realizó correctamente, pero no se encontraron datos adicionales para actualizar.'),
                    'type': 'info',
                    'sticky': False,
                }
            }
