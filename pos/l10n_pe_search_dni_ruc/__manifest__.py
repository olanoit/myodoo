# -*- coding: utf-8 -*-

{
    'name': 'Búsqueda RUC/DNI',
    'category': 'Uncategorized',
    'summary': 'Validación y Búsqueda de RUC/DNI para Perú',
    'description': """
		Este módulo facilita la búsqueda, validación y actualización de datos de RUC y DNI en Perú utilizando servicios de terceros como ApiPerú, ApiMigo y JSON-PE. Permite a los usuarios acceder a información verificada al ingresar o actualizar datos de contacto.

		**Características Principales:**
		- **Búsqueda Automática:** Realiza búsquedas automáticas de RUC y DNI al ingresar el número.
		- **Validación en Tiempo Real:** Verifica la validez de los RUC y DNI, incluyendo el estado y la condición del contribuyente.
		- **Actualización de Datos:** Actualiza automáticamente campos de contacto basándose en datos obtenidos de fuentes externas.

		**Beneficios:**
		- **Precisión de Datos:** Asegura que la información de contacto esté sincronizada con fuentes oficiales.
		- **Eficiencia Operativa:** Ahorra tiempo al automatizar la verificación y actualización de datos fiscales.
		- **Cumplimiento Regulatorio:** Facilita el cumplimiento de normativas al mantener actualizada la información de contribuyentes en Perú.

		Ideal para empresas que gestionan un alto volumen de contactos en Perú y requieren una herramienta confiable para validar y mantener actualizada la información de RUC y DNI.
		""",
    'author': 'Smartnet Technologies',
    'version': '1.0',
    'depends': ['base', 'base_vat', 'l10n_latam_base', 'l10n_pe'],
    'data': [
		'views/company_view.xml',
		'views/res_partner_view.xml',
	],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images':['static/description/banner.png'],
}
