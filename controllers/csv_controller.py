import pandas as pd
import requests
from dotenv import load_dotenv
import os
from io import StringIO
import json
from datetime import datetime

load_dotenv()  # Carga las variables de entorno desde el archivo .env

with open('resultados_ejemplos.json', 'r', encoding='utf-8') as f:
    ejemplos = json.load(f)

class CSVController:
    def __init__(self, file):
        self.file = file
        self.df = self.read_csv() if file else None

    def read_csv(self):
        if self.file:
            # Lee el contenido del archivo y conviértelo en un DataFrame
            content = self.file.stream.read().decode("utf-8")
            return pd.read_csv(StringIO(content))
        else:
            return None

    def get_csv_info(self):
        # Devuelve la información del DataFrame cargado
        #return self.df if self.df is not None else "No se ha cargado ningún archivo CSV"
        return self.df.to_json(orient="records", lines=True) if self.df is not None else "No se ha cargado ningún archivo CSV"
    
    def get_prompt_info(self, prompt):
        csv_info = self.get_csv_info()
        prompt += f"\nDatos del CSV:\n{csv_info.head()}"
        return prompt

    def process_data(self, prompt, ai_provider):
         # Obtener información del CSV si está cargado
        if self.df is not None:
            csv_info = self.get_csv_info()
            # Añadir la información del CSV al prompt
            #prompt += f"\nDatos del CSV:\n{csv_info.head()}"  # Aquí puedes personalizar cómo quieres añadir la información
            prompt += f"\nDatos del CSV:\n{csv_info}"  # Aquí puedes personalizar cómo quieres añadir la información
        else:
            prompt += "\nNo se ha cargado ningún archivo CSV"

        # Llamada a la API de la IA seleccionada
        if ai_provider == "seleccione":
            response = prompt
        elif ai_provider == "ejemploVideo":
            response = "chatgpt.com: \n\n ### Resumen General del Número Total de Incidentes \nEl archivo CSV proporcionado contiene un total de **12 registros de incidentes de seguridad** detectados por el SIEM. \n \n### Tipos de Incidentes Más Comunes y su Frecuencia \nLos incidentes en el archivo están relacionados principalmente con consultas DNS, específicamente: \n \n- **Consultas DNS tipo 'A'**: 6 incidentes (50% del total) \n- **Consultas DNS tipo 'AAAA'**: 6 incidentes (50% del total) \n \n### Fuentes Más Frecuentes de los Ataques \nLas direcciones IP involucradas como fuentes de las consultas DNS son: \n- **10.100.1.95**: Aparece en 4 incidentes \n- **10.100.0.2**: Aparece en 4 incidentes \n- **10.100.1.186**: Aparece en 4 incidentes \n- **10.100.1.105**: Aparece en 4 incidentes \n \n### Patrones Notables o Tendencias en los Datos \n1. **Frecuencia Temporal**: Todos los incidentes ocurrieron en un intervalo muy corto, específicamente entre las 17:13:14 y las 17:13:17 del 16 de mayo de 2021, lo que sugiere una ráfaga de actividad relacionada con consultas DNS. \n2. **Destino Común**: Todas las consultas están dirigidas al mismo dominio, `ssm.us-east-2.amazonaws.com`. \n3. **Respuestas DNS**: Solo las consultas tipo 'A' obtuvieron respuestas, mientras que todas las consultas tipo 'AAAA' no recibieron ninguna respuesta. \n4. **Repetición de Consultas**: Las mismas consultas DNS se repiten entre las diferentes fuentes IP. \n \n### Recomendaciones para Mejorar la Seguridad Basadas en los Datos Proporcionados \n1. **Monitoreo de DNS**: Fortalecer el monitoreo de las consultas DNS para identificar patrones inusuales y potencialmente maliciosos, especialmente para dominios externos. \n2. **Análisis de Direcciones IP**: Revisar las direcciones IP internas (10.100.1.95, 10.100.1.186, 10.100.1.105) para asegurarse de que no estén comprometidas y de que los dispositivos asociados estén correctamente configurados y protegidos. \n3. **Filtros y Políticas DNS**: Implementar filtros y políticas que bloqueen o restrinjan consultas a dominios externos no autorizados o sospechosos. \n4. **Capacitación y Concientización**: Aumentar la capacitación de los empleados en buenas prácticas de seguridad para reducir la posibilidad de que dispositivos internos sean utilizados para actividades maliciosas. \n5. **Auditoría de Seguridad**: Realizar auditorías periódicas de seguridad para detectar y mitigar cualquier vulnerabilidad que pueda ser explotada en ataques futuros. \n6. **Actualización de Software**: Asegurar que todos los sistemas y dispositivos estén actualizados con los últimos parches de seguridad para prevenir vulnerabilidades explotables.\n\nEste análisis muestra la importancia de la vigilancia continua y la implementación de medidas proactivas de seguridad para proteger la infraestructura de la empresa frente a amenazas potenciales."
        elif ai_provider == "ejemplo1":
            #text = json.dumps(ejemplos, indent=4)
            #response = text
            response = "Ejemplos: \n\n"
            response += "phi-3-small-8k-instruct: \n A suspicious DNS activity was detected involving multiple IP addresses, including '10.100.1.26', '10.100.1.95', '10.100.1.186', and '10.100.1.105'. The source IP '141.212.123.189' was also involved in the DNS queries.    The DNS queries were initiated by the source IP '141.212.123.189' towards the IP '10.100.1.26'. The queried domain name was 'researchscan541.eecs.umich.edu'. Although the DNS response code and operation code were 0, indicating no issues, the high number of DNS queries from a single source IP and the involvement of multiple IP addresses raise suspicion.        Following this, there were multiple DNS queries and responses between the IP addresses '10.100.1.26', '10.100.1.95', '10.100.1.186', and '10.100.1.105'. The number of answers in the DNS responses was either 1 or 0, suggesting possible DNS tunneling or information exfiltration attempts.        In conclusion, the detected DNS activity indicates a potential security threat involving multiple IP addresses and suspicious DNS queries, which should be further investigated to prevent any potential security breaches.\n\n"
            response += "gemini-1.5-flash-api-0514: \n Los datos del CSV muestran un patrón de consultas DNS con el nombre ssm.us-east-2.amazonaws.com desde diferentes IPs de origen (10.100.1.95, 10.100.1.186, 10.100.1.105, 10.100.1.26, 10.100.1.4) hacia la IP de destino 10.100.0.2.     Este patrón sugiere que se están intentando resolver las direcciones IP del servicio AWS Systems Manager (SSM) desde diferentes dispositivos dentro de la red.         El problema podría ser:        * **Escaneo de red:** Un atacante podría estar explorando la red para identificar dispositivos que ejecutan SSM y luego explotar vulnerabilidades en el servicio.    * **Acceso no autorizado:** Un usuario no autorizado podría estar intentando acceder a recursos de la red a través de SSM.    * **Comportamiento malicioso:** Los dispositivos podrían estar comprometidos y realizando consultas DNS maliciosas para comunicarse con un servidor de comando y control.         Es necesario investigar más a fondo para determinar la causa exacta de este comportamiento y tomar medidas para mitigar el riesgo.\n\n"
            response += "gpt-4-0613: \n Los datos proporcionados parecen ser registros de consultas y respuestas DNS entre diferentes direcciones IP dentro de una red local. Las consultas DNS se realizan a ssm.us-east-2.amazonaws.com, que es un dominio de Amazon Web Services (AWS). En general, las consultas DNS son normales en una red, ya que los sistemas necesitan resolver los nombres de dominio en direcciones IP para comunicarse con ellos.    Sin embargo, hay un caso en el que la dirección IP 141.212.123.189 consulta el dominio researchscan541.eecs.umich.edu. Este evento es diferente de los demás y puede ser una señal de actividad sospechosa o no autorizada. La dirección IP en cuestión parece estar asociada con la Universidad de Michigan, y este tipo de consultas podría ser una señal de un intento de escaneo de red o de otro tipo de actividad de reconocimiento.        En resumen, la mayoría de los eventos parecen ser tráfico normal de red, pero el evento relacionado con la consulta al dominio researchscan541.eecs.umich.edu puede ser señal de actividad sospechosa y podría requerir una investigación más a fondo."
        elif ai_provider == "ejemplo2":
            #text = json.dumps(ejemplos, indent=4)
            #response = text
            response = "Ejemplos: \n\n"
            response += "gpt-4-turbo-2024-04-09: \n Los datos extraídos del CSV parecen estar enfocados principalmente en la actividad de DNS dentro de una red, específicamente alrededor de las consultas DNS para el dominio 'ssm.us-east-2.amazonaws.com', que es un servicio de Amazon AWS (Amazon Simple Systems Manager en la región de US East 2). A continuación, se detalla un resumen de la actividad observada y los problemas potenciales asociados: ### Resumen del Evento- **Fecha y Hora:** Los eventos se registraron en múltiples instancias el 16 de mayo de 2021, con tiempos que varían a lo largo del día.- **IPs Involucradas:** Varias direcciones IP internas (como 10.100.1.95, 10.100.1.186, etc.) interactúan con una dirección IP interna específica (10.100.0.2) que parece actuar como un servidor DNS o un gateway.- **Consultas DNS:** Se realizaron consultas tanto de tipo 'A' (que resuelve a direcciones IPv4) como de tipo 'AAAA' (que resuelve a direcciones IPv6), todas dirigidas al mismo dominio relacionado con AWS.- **Respuestas DNS:** En algunos casos, no se recibieron respuestas (Número de respuestas = 0), mientras que en otros, se proporcionaron direcciones IP específicas como respuestas con diferentes TTLs (Time to Live).### Problemas Potenciales1. **Fallas de Resolución de DNS:** La presencia de múltiples consultas sin respuesta sugiere posibles problemas con la resolución de DNS dentro de la red. Esto podría ser indicativo de problemas de configuración en el servidor DNS, problemas de red que impiden la resolución de DNS, o un posible ataque de denegación de servicio (DoS) que busca sobrecargar el servidor DNS.2. **Uniformidad en las Consultas de Destino:** La repetición en las consultas hacia un mismo dominio de AWS podría indicar una configuración automatizada o scripts que intentan constantemente acceder a recursos de AWS. Si bien esto podría ser una operación legítima, también es susceptible a ser un vector para actividades maliciosas como la exfiltración de datos si no se maneja adecuadamente.3. **Seguridad y Supervisión:** La ausencia de indicadores de malicia (`evil = 0` en todos los casos) y señales de alerta (`sus = 0` en la mayoría excepto uno) es positiva, pero la constante verificación y falta de respuestas sugiere que podría ser prudente revisar la seguridad perimetral y los sistemas de detección de intrusiones para asegurar que no se están perdiendo actividades sospechosas.### Acciones Recomendadas- **Revisión de Configuración de DNS:** Verificar la configuración del servidor DNS para asegurarse de que está optimizado y puede manejar las solicitudes eficientemente.- **Monitoreo Continuo:** Asegurarse de que los sistemas de monitoreo y alerta estén funcionales y bien configurados para detectar patrones anómalos que pudieran indicar problemas de seguridad.- **Validación de Tráfico:** Confirmar que todas las consultas a servicios de AWS y respuestas son legítimas y corresponden a operaciones de negocio esperadas, minimizando así la posibilidad de uso malicioso de los recursos de la red.Estos pasos ayudarán a mitigar los problemas potenciales y asegurarán la integridad y la seguridad de la infraestructura de TI de la red observada.\n\n"
            response += "chatgpt.com: \n Based on the provided CSV data extracted from security events, let's summarize the detected event and the associated problem:    ### Detected Event:    - **Timestamp:** 2021-05-16T17:13:14Z    - **Source IP:** 10.100.1.95    - **Destination IP:** 10.100.0.2    - **DNS Query:** ssm.us-east-2.amazonaws.com    - **DNS Response:** 52.95.19.240 (Resolved IP)    - **DNS Query Type:** A (IPv4 Address)    - **Number of Answers:** 1        ### Problem Identified:    - **Summary:** The event involves a DNS query for `ssm.us-east-2.amazonaws.com` from source IP `10.100.1.95` to destination IP `10.100.0.2`, resulting in a successful resolution (`A` record type) to IP address `52.95.19.240`.    - **Potential Issue:** While the DNS query itself may not indicate an immediate problem, the frequency or pattern of such queries could be suspicious. In a security context, this could hint at reconnaissance or data exfiltration attempts targeting AWS services (`ssm.us-east-2`), possibly indicating unauthorized access or attempts to exploit AWS resources.        ### Context:    - AWS System Manager (`ssm.us-east-2.amazonaws.com`) is commonly used for managing AWS resources, including instances, applications, and services. Unauthorized queries or excessive queries from internal IPs (`10.100.x.x` in this case) could suggest internal reconnaissance or potential exploitation.    - Monitoring and analyzing the pattern of such queries, especially when resolved IPs are external and not expected, is crucial for identifying and mitigating security risks within the AWS infrastructure.        ### Recommendation:    - **Immediate Action:** Review logs and network traffic to identify any anomalous patterns or spikes in similar DNS queries.    - **Enhanced Security Measures:** Implement stricter access controls and monitoring mechanisms for AWS services, including AWS System Manager, to detect and prevent unauthorized access attempts.    - **Regular Audits:** Conduct regular audits of AWS permissions and configurations to ensure compliance and security best practices.        By addressing these aspects, you can enhance the security posture and mitigate risks associated with potential unauthorized access or exploitation attempts targeting AWS resources.\n\n"
            response += "https://g.co/gemini/share/a2b94254d447 VERSION 1: \n ## Resumen de los eventos de seguridad detectados    **Eventos:**        Se observan varios eventos en los que una dirección IP (10.100.1.95, 10.100.1.186, 10.100.1.105, 10.100.1.26, 10.100.1.4) realiza consultas DNS a un dominio específico (ssm.us-east-2.amazonaws.com) y recibe respuestas que incluyen direcciones IP adicionales. Este patrón de comportamiento podría indicar una actividad de **envenenamiento de DNS** o **reconnaissance**.        **Impacto:**        El envenenamiento de DNS puede redirigir el tráfico de los usuarios a sitios web maliciosos o comprometer la confidencialidad de los datos. La reconnaissance se utiliza para recopilar información sobre una red o sistema con el fin de identificar vulnerabilidades y preparar ataques.        **Recomendaciones:**        * Implementar medidas de seguridad DNS, como **DNSSEC** o **validación de origen**, para evitar el envenenamiento de DNS.    * Monitorear el tráfico de red y las consultas DNS para detectar actividades anómalas.    * Mantener los sistemas y el software actualizados con los últimos parches de seguridad.    * Implementar controles de acceso estrictos y educar a los usuarios sobre las amenazas de seguridad cibernética.        **Información adicional:**        * Los eventos se detectaron en diferentes fechas y horas, lo que sugiere que la actividad pudo haber ocurrido en varias ocasiones.    * Algunas de las direcciones IP de destino (52.95.19.240, 52.95.21.209, 52.95.22.56) no parecen estar asociadas con Amazon Web Services, lo que aumenta la sospecha de actividad maliciosa.    * Los registros de firewall y IDS/IPS no muestran alertas relacionadas con estos eventos, lo que puede indicar que la actividad eludió las medidas de seguridad existentes.        **Es importante tener en cuenta que esta es solo una breve descripción de los eventos detectados. Se recomienda un análisis más profundo para determinar la naturaleza exacta de la amenaza y tomar las medidas de mitigación adecuadas.**    \n\n"
            response += "https://g.co/gemini/share/a2b94254d447 VERSION 2: \n ## Resumen de los eventos de seguridad detectados:    **Eventos:** Se observan varios intentos de consultas DNS entre diferentes direcciones IP. Las consultas se realizan para obtener las direcciones IP asociadas a nombres de dominio específicos (por ejemplo, ssm.us-east-2.amazonaws.com).         **Problema:** La cantidad y la frecuencia de estas consultas sugieren que podrían ser parte de un ataque de DNS Spoofing o de un intento de enumerar hosts en la red.         **Evidencia:**        * Se observan consultas DNS desde varias direcciones IP diferentes.    * Las consultas se realizan para una variedad de nombres de dominio relacionados con Amazon Web Services (AWS).    * Algunos de los nombres de dominio resueltos no coinciden con las direcciones IP esperadas.        **Impacto potencial:**        * Un ataque de DNS Spoofing podría redirigir el tráfico a sitios web maliciosos o comprometer la comunicación entre hosts.    * La enumeración de hosts puede revelar información valiosa a los atacantes, que podrían usarla para lanzar otros ataques.        **Recomendaciones:**        * Implementar medidas de seguridad DNS, como DNSSEC o validación de DNS.    * Monitorear las consultas DNS de cerca para detectar actividades anormales.    * Considerar la implementación de un sistema de detección de intrusos (IDS) o un sistema de prevención de intrusos (IPS) para la red.        **Información adicional:**        * Los eventos se registraron entre el 16 de mayo de 2021 y el 27 de junio de 2024.    * Los eventos se detectaron en varios firewalls y servidores diferentes.    * La información proporcionada es solo un resumen y no incluye todos los detalles de los eventos.        **Es importante tener en cuenta que esta información es solo para fines informativos y no debe considerarse como un consejo de seguridad definitivo. Se recomienda consultar con un experto en seguridad para obtener una evaluación completa de su red y para implementar las medidas de seguridad adecuadas.**    \n\n"
            response += "https://g.co/gemini/share/a2b94254d447 VERSION 3: \n ## Resumen de los eventos de seguridad detectados**Fechas:** 16 de mayo de 2021**Fuente:** Los datos se extrajeron de un archivo CSV que contiene información de eventos de seguridad.**Resumen:*** Se observaron varios intentos de consultas DNS entre diferentes direcciones IP. Las consultas se realizaron para el dominio 'ssm.us-east-2.amazonaws.com'.* Las respuestas a las consultas DNS incluyeron direcciones IP tanto IPv4 como IPv6.* Algunos de los eventos generaron alertas por parte de firewalls e IDS/IPS.* Los eventos se detectaron en diferentes ubicaciones geográficas.**Problema:*** La naturaleza exacta de la amenaza no se puede determinar con los datos proporcionados.* Sin embargo, la actividad observada es consistente con un posible intento de **envenenamiento de DNS** o **ataque de hombre en el medio (MitM)**.* En este tipo de ataques, los actores maliciosos intentan interceptar y manipular las comunicaciones DNS para redirigir el tráfico a sitios web falsos o maliciosos.**Recomendaciones:*** Se recomienda realizar un análisis más detallado de los eventos para determinar la naturaleza exacta de la amenaza.* Se deben implementar medidas de seguridad adecuadas para mitigar el riesgo de ataques de envenenamiento de DNS y MitM, como:    * **Usar DNSSEC:** DNSSEC es un conjunto de extensiones de seguridad para el sistema de nombres de dominio (DNS) que agrega autenticación e integridad a las comunicaciones DNS.    * **Habilitar HSTS:** HSTS (HTTP Strict Transport Security) es una política de seguridad web que obliga a los navegadores web a usar siempre HTTPS para comunicarse con un sitio web específico.    * **Usar un firewall de red:** Un firewall de red puede ayudar a bloquear el tráfico no autorizado y malicioso.    * **Mantener el software actualizado:** Es importante mantener el software del sistema operativo, los navegadores web y las aplicaciones antivirus actualizados con los últimos parches de seguridad.**Nota:*** La información proporcionada en este resumen se basa en un análisis limitado de los datos disponibles. Se recomienda realizar una investigación más profunda para comprender completamente la naturaleza y el alcance de la amenaza."
        elif ai_provider == "chatgpt":
            response = self.call_chatgpt_api(prompt)
        elif ai_provider == "openllama":
            response = self.call_openllama_api(prompt)
        else:
            response = "Proveedor de IA no válido"

        # Almacenar los resultados en un archivo JSON
        self.save_results_to_json(prompt, response)

        return response

    def call_chatgpt_api(self, prompt):
        # Reemplaza con tu API Key de OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def call_openllama_api(self, prompt):
        # Reemplaza con la URL de tu instancia de OpenLLaMA
        api_url = os.getenv("OPENLLAMA_API_URL")
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    def save_results_to_json(self, prompt, results):
        # Crear un diccionario con los datos a almacenar
        data = {
            "prompt": prompt,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

        # Generar el nombre del archivo de resultados con la fecha actual
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"resultados_{current_date}.json"

        # Obtener la ruta completa de la carpeta 'resultados' y el archivo
        folder_path = os.path.join(os.getcwd(), "resultados")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, filename)

        # Guardar el diccionario como JSON en el archivo
        with open(file_path, "a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.write("\n")


