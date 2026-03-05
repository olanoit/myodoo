# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import unicodedata
from . import search_service


def _normalize_text(text):
    return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").strip().upper().decode()

class Partner(models.Model):
    _inherit = 'res.partner'

    doc_type = fields.Char(related="l10n_latam_identification_type_id.l10n_pe_vat_code", store=True)
    doc_number = fields.Char(_("Document Number"))
    commercial_name = fields.Char(_("Commercial Name"), default="-")
    legal_name = fields.Char(_("Legal Name"), default="-")
    state = fields.Selection(search_service.STATE, string=_('Status'), default="ACTIVO")
    condition = fields.Selection(search_service.CONDITION, string=_('Condition'), default='HABIDO')
    is_validate = fields.Boolean(_("Is Validated"))
    last_update = fields.Datetime(_("Last Update"))
    good_contributor = fields.Boolean(_('Good Contributor'))
    is_retention_agent = fields.Boolean(_('Is Retention Agent'))
    from_date = fields.Date(_('From Date'))
    resolution = fields.Char(_('Resolution'))

    auto_search = fields.Boolean(_("Automatic Search"), default=True, help=_("If selected, the RUC or DNI data will be searched on SUNAT when entered or changed"))

    @api.model
    def default_get(self, fields_list):
        res = super(Partner, self).default_get(fields_list)
        if 'country_id' in fields_list and not res.get('country_id'):
            peru = self.env.ref('base.pe', raise_if_not_found=False)
            if peru:
                res['country_id'] = peru.id
        if 'l10n_latam_identification_type_id' in fields_list and not res.get('l10n_latam_identification_type_id'):
            ruc_type = self.env.ref('l10n_pe.it_RUC', raise_if_not_found=False)
            if ruc_type:
                res['l10n_latam_identification_type_id'] = ruc_type.id
        return res

    def simple_data_query(self, document_type, document_number):
        partner_record = self.search([('vat', '=', document_number)])
        
        if partner_record.exists():
            field_name = 'names' if document_type in ["dni", "01", "1"] else 'business_name'
            data_json = {
                'success': True,
                'data': {
                    field_name: partner_record.display_name
                }
            }
            return {'error': False, 'message': None, 'data': data_json}
        
        return {'error': True, 'message': _('Document not found'), 'data': {}}

    @api.constrains("doc_number")
    def check_doc_number(self):
        for partner in self:
            if partner.parent_id:
                continue

            doc_type = partner.l10n_latam_identification_type_id.l10n_pe_vat_code
            doc_number = partner.doc_number

            if not doc_type and not doc_number:
                continue

            if not doc_number:
                raise ValidationError(_("Please enter the document number"))

            if doc_type == '6' and not self.validate_ruc(doc_number):
                raise ValidationError(_('The entered RUC is incorrect'))

            if self.search_count([
                ('company_id', '=', partner.company_id.id),
                ('l10n_latam_identification_type_id.l10n_pe_vat_code', '=', doc_type),
                ('doc_number', '=', doc_number)
            ]) > 1:
                raise ValidationError(_('The document number already exists and violates the unique field constraint'))

    @api.onchange('company_type')
    def _onchange_company_type(self):
        if self.company_type == 'company':
            ruc_type = self.env.ref('l10n_pe.it_RUC', raise_if_not_found=False)
            if ruc_type:
                self.l10n_latam_identification_type_id = ruc_type.id
        else:
            dni_type = self.env.ref('l10n_pe.it_DNI', raise_if_not_found=False)
            if dni_type:
                self.l10n_latam_identification_type_id = dni_type.id
        self.vat = False
        self.doc_number = False

    @api.onchange('l10n_latam_identification_type_id')
    def _onchange_identification_type(self):
        if self.l10n_latam_identification_type_id:
            vat_code = self.l10n_latam_identification_type_id.l10n_pe_vat_code
            self.company_type = 'company' if vat_code == "6" else 'person'
            self.vat = False
            self.doc_number = False

    @staticmethod
    def validate_ruc(vat):
        if len(vat) == 11 and vat.isdigit():
            factor = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
            total_sum = sum(int(vat[i]) * factor[i] for i in range(10))
            return int(vat[10]) == (11 - (total_sum % 11)) % 10
        return False

    @api.onchange("vat")
    def _onchange_vat(self):
        if self.vat:
            self.doc_number = self.vat

    @api.onchange("doc_number")
    def _onchange_doc_number(self):
        if self.doc_number:
            self.vat = self.doc_number

    @api.onchange("doc_number", "vat", "l10n_latam_identification_type_id")
    @api.depends("l10n_latam_identification_type_id", "doc_number", "vat")
    def _doc_number_change(self):
        if not self.auto_search:
            return

        self._validate_document_type()
        token, search_type = self._get_token_and_search_type()
        
        vat = self.vat.strip() if self.vat else ""
        vat_type = self.l10n_latam_identification_type_id.l10n_pe_vat_code

        process_functions = {
            "1": self._process_dni,
            "6": self._process_ruc
        }
        
        process_function = process_functions.get(vat_type)
        if vat and process_function:
            process_function(token, vat, search_type)


    def _get_token_and_search_type(self):
        if self.company_id:
            return self.company_id.token, self.company_id.vat_search_api
        return self.env.company.token, self.env.company.vat_search_api

    def _process_dni(self, token, vat, search_type):
        if len(vat) != 8:
            raise UserError(_("The entered DNI is incorrect"))
        
        search_functions = {
            "apiperu": search_service.fetch_dni_from_apiperu,
            "apimigo": search_service.fetch_dni_from_apimigo,
            "jsonpe": search_service.fetch_dni_from_jsonpe
        }

        fetch_function = search_functions.get(search_type)
        if not fetch_function:
            raise UserError(_("Invalid search type specified"))

        response = fetch_function(token, vat)
        if response:
            self._set_dni_data(response)

    def _set_dni_data(self, name):
        self.name = name
        self.company_type = "person"
        self.is_validate = True
        self.country_id = 173
        self._set_location("Lima", "Lima")

    def _process_ruc(self, token, vat, search_type):
        if not self.validate_ruc(vat):
            raise UserError(_("The entered RUC is incorrect"))

        vals = self._fetch_ruc_data(token, vat, search_type)
        self._set_ruc_data(vals)

    def _fetch_ruc_data(self, token, vat, search_type):
        search_functions = {
            "apiperu": search_service.fetch_ruc_from_apiperu,
            "apimigo": search_service.fetch_ruc_from_apimigo,
            "jsonpe": search_service.fetch_ruc_from_jsonpe
        }

        fetch_function = search_functions.get(search_type)
        if not fetch_function:
            raise UserError(_("Invalid search type specified"))

        for _ in range(3):
            vals = fetch_function(token, vat)
            if not vals.get("error"):
                return vals

        raise UserError(vals.get("message", _("Operation could not be completed")))



    def _set_ruc_data(self, vals):
        self.commercial_name = vals.get("company_name")
        self.legal_name = vals.get("company_name")
        self.name = vals.get("company_name")
        self.street = vals.get("address")
        self.company_type = "company"
        self.state = vals.get("status")
        self.condition = vals.get("condition")
        self.is_validate = True
        

        if vals.get("buen_contribuyente"):
            self.good_contributor = vals["buen_contribuyente"]
            self.from_date = vals.get("a_partir_del")
            self.resolution = vals.get("resolucion")

        self._set_location(vals.get("distrito"), vals.get("provincia"), vals.get("ubigeo"))


    def _set_location(self, district, province, ubigeo=None):
        district_obj = self.env["l10n_pe.res.city.district"]
        district_record = None
        if ubigeo:
            district_record = district_obj.search([("code", "=", ubigeo)], limit=1)
        elif district and province:
            normalized_district = _normalize_text(district)
            normalized_province = _normalize_text(province)
            district_record = self._search_district(district_obj, normalized_district, normalized_province)

        if district_record:
            self.l10n_pe_district = district_record.id
            self.city_id = district_record.city_id.id
            self.state_id = district_record.city_id.state_id.id
            self.zip = district_record.code
            self.country_id = district_record.city_id.state_id.country_id.id

    def _search_district(self, district_obj, district, province):
        district_record = district_obj.search([("name", "=ilike", district), ("city_id", "!=", False)])
        if len(district_record) > 1:
            district_record = district_obj.search([("name", "=ilike", district), ("city_id.name", "=ilike", province)])
        if len(district_record) != 1:
            raise Warning(_("Could not establish district code, options not found or multiple results"))
        return district_record

    def _validate_document_type(self):
        vat = self.vat if self.vat and len(self.vat) >= 1 else ""
        doc_type = self.l10n_latam_identification_type_id.l10n_pe_vat_code or None
        self.doc_type = "7" if not vat else self._get_doc_type(vat, doc_type)

    def _get_doc_type(self, vat, doc_type):
        validations = {
            "0": lambda vat: "0",
            "1": self._validate_dni,
            "4": lambda vat: "4",
            "6": self._validate_ruc,
            "A": lambda vat: "A"
        }
        return validations.get(doc_type, lambda vat: self._raise_invalid_type())(vat)    
    
    def _validate_ruc(self, vat):
        if not self.validate_ruc(vat):
            raise UserError(_("The entered RUC is incorrect"))
        return "6"
    
    def _validate_dni(self, vat):
        if len(vat) != 8 or not vat.isdigit():
            raise UserError(_("The entered DNI is incorrect"))
        return "1"

    def _raise_invalid_type(self):
        raise UserError(_("Invalid or unsupported document type"))

    @api.onchange('country_id')
    def _onchange_country(self):
        pass

    @api.onchange('l10n_pe_district')
    def _onchange_district_id(self):
        if self.l10n_pe_district:
            self.zip = self.l10n_pe_district.code
            self.city_id = self.city_id or self.l10n_pe_district.city_id.id

    @api.onchange('city_id')
    def _onchange_province_id(self):
        return {
            'domain': {
                'l10n_pe_district': [('city_id', '=', self.city_id.id)] if self.city_id else []
            }
        }

    @api.onchange('state_id')
    def _onchange_state_id(self):
        return {
            'domain': {
                'city_id': [('state_id', '=', self.state_id.id)] if self.state_id else []
            }
        }

    @api.model
    def change_commercial_name(self):
        partners = self.search([('commercial_name', '!=', '-'), ('doc_type', '=', '6')])
        partners.update_document()

    def update_document(self):
        self._doc_number_change()
        self._onchange_district_id()
