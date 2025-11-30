# OCR Manager - IA Generativa para Odoo

![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple?style=flat-square)
![License](https://img.shields.io/badge/License-OPL--1-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green?style=flat-square)

**OCR Manager** transforma la digitalización de documentos en Odoo reemplazando el OCR tradicional por potentes modelos de **Inteligencia Artificial Generativa** (Google Gemini, OpenAI GPT-4o).

Este módulo te permite utilizar **tus propias API Keys**, eliminando el costo por crédito de Odoo IAP y ofreciendo una precisión superior en la lectura de facturas complejas, tickets y documentos no estructurados.

---

## ✨ Características Principales

* **🧠 IA Multimodal:** Integración nativa con **Google Gemini** (Flash/Pro) y **OpenAI** (GPT-4o) para "ver" y "entender" documentos.
* **🔌 Integración Transparente:** Funciona interceptando el botón nativo **"Digitalizar"** en las facturas de Odoo. El usuario no nota la diferencia, pero el motor es mucho más potente.
* **🚀 Carga Masiva (Bulk Wizard):** Asistente exclusivo para cargar y procesar lotes de 50, 100 o más facturas simultáneamente, con reporte de estado en tiempo real.
* **📝 Prompts Configurables:** Ajusta las instrucciones que recibe la IA directamente desde la interfaz de Odoo (sin tocar código) para mejorar la detección de campos específicos.
* **🇦🇷 Localización Inteligente:**
    * Detección y limpieza automática de números de comprobante (formato `PV-Numero` ej: `00001-00000040`) mediante Regex.
    * Mapeo inteligente de impuestos y partners.
    * Soporte específico para facturas de Argentina y LATAM.
* **📄 Motor PDF Avanzado:** Utiliza `PyMuPDF` para convertir PDFs a imágenes de alta resolución antes de enviarlos a la IA, garantizando nitidez incluso en escaneos difíciles.

---

## 🛠️ Requisitos e Instalación

### 1. Dependencias Python
# OCR Manager - IA Generativa para Odoo

![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple?style=flat-square)
![License](https://img.shields.io/badge/License-OPL--1-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green?style=flat-square)

**OCR Manager** transforma la digitalización de documentos en Odoo reemplazando el OCR tradicional por potentes modelos de **Inteligencia Artificial Generativa** (Google Gemini, OpenAI GPT-4o).

Este módulo te permite utilizar **tus propias API Keys**, eliminando el costo por crédito de Odoo IAP y ofreciendo una precisión superior en la lectura de facturas complejas, tickets y documentos no estructurados.

---

## 🛠️ Requisitos e Instalación

### 1. Dependencias Python
Este módulo requiere librerías externas para conectar con las IAs y procesar PDFs. Si usas **Odoo.sh**, estas se instalarán automáticamente gracias al `requirements.txt` incluido.

Para instalaciones On-Premise:
```bash
pip install google-genai>=0.3.0
pip install openai>=1.0.0
pip install pymupdf>=1.23.0  # Para procesar PDFs
```
### 2. Configuración en Odoo
Una vez instalado el módulo:
Ve a Ajustes $\rightarrow$ Compañías.
Accede a la pestaña "OCR Manager (IA)".
Activa la opción "Habilitar OCR Manager".
Selecciona tu proveedor (ej. Google Gemini) y pega tu API Key.
Modelo IA: Se recomienda usar gemini-1.5-flash-002 para mayor estabilidad y velocidad.

### 🚀 Manual de Uso
#### Método A: Factura Individual (Flujo Nativo)
Ideal para el día a día administrativo.
Ve a Contabilidad $\rightarrow$ Proveedores $\rightarrow$ Facturas.
Crea una nueva factura y sube tu PDF o imagen al "chatter" (zona de adjuntos a la derecha).
Haz clic en el botón "Digitalizar" (o "Solicitar Digitalización").
En pocos segundos, la IA completará: Partner, Fechas, Número de Factura, Líneas de producto e Impuestos.

#### Método B: Carga Masiva (Wizard)
Ideal para procesar lotes de facturas a fin de mes.
Ve a Contabilidad $\rightarrow$ Proveedores $\rightarrow$ Digitalización Masiva IA.
Haz clic en "Agregar Línea" y sube tus archivos (uno por línea).
Presiona el botón "🚀 Procesar Todo".
El sistema procesará los archivos uno por uno.
Verás un indicador verde (Éxito) o rojo (Error) por cada archivo.
Podrás navegar directamente a las facturas creadas desde el asistente.

### ⚙️ Personalización Técnica (Prompts)
¿La IA no está leyendo bien un campo específico de tu industria? Puedes ajustar las instrucciones:
Activa el Modo Desarrollador.
Ve a Ajustes $\rightarrow$ Técnico $\rightarrow$ OCR Manager $\rightarrow$ Prompts IA.
Selecciona el prompt activo (ej: gemini_invoice).
Edita el texto del prompt.
Ejemplo: Puedes agregar "Si encuentras un número de remito, guárdalo en el campo referencia interna".
Guarda. El cambio aplica inmediatamente para las siguientes digitalizaciones.

### 🏗️ Arquitectura del Módulo
Este módulo sigue una arquitectura de "Cerebro Centralizado" para facilitar el mantenimiento:
*   `models/extract_mixin.py`: Contiene toda la lógica de conexión API, conversión de imágenes y parseo de datos. Cualquier mejora aquí impacta en todo el sistema.
*   `wizard/ocr_bulk_digitize_wizard.py`: Orquestador ligero. No contiene lógica de IA, simplemente crea facturas y delega el procesamiento al Mixin.
*   `models/ocr_prompt.py`: Modelo para la persistencia y gestión de prompts dinámicos.

### Créditos
Desarrollado por: AlparData & Gemini