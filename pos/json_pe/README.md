# JSON.PE - Consulta DNI y RUC

## Descripción

Este módulo integra Odoo con la API de **json.pe** para consultar información de DNI y RUC peruanos directamente desde el formulario de contactos (Partners). Permite autocompletar automáticamente los datos del contacto con la información obtenida de la API.

### Características principales:
- Consulta de DNI (Documento Nacional de Identidad) desde el formulario de Partner
- Consulta de RUC (Registro Único de Contribuyente) desde el formulario de Partner
- Autocompletado automático de campos: nombre, dirección, ciudad, código postal, etc.
- Validación de formatos (DNI: 8 dígitos, RUC: 11 dígitos)
- Manejo de errores y mensajes informativos

---

## Configuración del API Token

Antes de usar el módulo, es necesario crear una cuenta en app.json.pe y obtener tu API Token:

### Paso 1: Crear cuenta en app.json.pe

1. Visita [https://app.json.pe](https://app.json.pe)
2. Haz clic en **Registrarse** o **Crear cuenta**
3. Completa el formulario de registro con tus datos
4. Verifica tu cuenta siguiendo las instrucciones que recibirás por correo electrónico
5. Inicia sesión en tu cuenta

### Paso 2: Obtener el API Token

1. Una vez dentro de tu cuenta en app.json.pe, navega a la sección de **API Tokens** o **Tokens**
2. Haz clic en **Generar Token** o **Crear nuevo token**
3. Copia el token generado (guárdalo en un lugar seguro, ya que no podrás verlo nuevamente)

### Paso 3: Configurar el token en Odoo

1. Ve a **Configuración** (Settings) → **Configuración General** (General Settings)
2. Busca la sección **JSON.PE - Consulta DNI y RUC**
3. En el campo **API Token**, pega el token que copiaste desde app.json.pe
4. Haz clic en **Guardar** (Save)

> **Nota:** Si no tienes una cuenta, créala en [https://app.json.pe](https://app.json.pe)

---

## Uso de los Botones DNI/RUC

### Consultar DNI

1. Abre o crea un contacto (Partner) en Odoo
2. Ingresa el **DNI** (8 dígitos) en el campo correspondiente
3. Haz clic en el botón **"Consultar DNI"** ubicado en el encabezado del formulario
4. El sistema consultará la API y autocompletará automáticamente:
   - Nombre completo

### Consultar RUC

1. Abre o crea un contacto (Partner) en Odoo
2. Ingresa el **RUC** (11 dígitos) en el campo correspondiente
3. Haz clic en el botón **"Consultar RUC"** ubicado en el encabezado del formulario
4. El sistema consultará la API y autocompletará automáticamente:
   - Nombre o Razón Social
   - Número de identificación fiscal (RUC)
   - Dirección completa
   - Ciudad/Distrito
   - Código postal (Ubigeo)

> **Importante:** Los botones solo aparecerán si has ingresado un DNI o RUC válido en el formulario.

---

## Enlaces

- **API JSON.PE:** [https://json.pe](https://json.pe)
- **Documentación:** [https://json.pe/docs](https://json.pe/docs)

---

## Requisitos

- Odoo 17.0
- Módulo `contacts` instalado
- Biblioteca Python `requests`
- Conexión a internet
- API Token válido de json.pe

---

## Soporte

Para más información sobre la API de json.pe, visita [https://json.pe](https://json.pe)
