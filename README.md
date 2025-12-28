# 🤖 WhatsApp Bot Colombiano "Deep" 🇨🇴

Un bot de WhatsApp con personalidad colombiana "chévere", construido con Python, Twilio, Docker y Ngrok, listo para ejecutarse localmente sin instalar nada en tu máquina.

## ✨ Características

- ✅ **Personalidad colombiana auténtica**: Saludos como "¡Quiubo parce!" y explicaciones de jerga como "chévere" y "bacano"
- ✅ **Arquitectura profesional**: Código limpio siguiendo principios SOLID, responsabilidad única y buenas prácticas
- ✅ **Contenedores Docker**: Todo corre en contenedores (bot, ngrok, tests) - nada se instala en tu sistema
- ✅ **Configuración centralizada**: Todas las credenciales se manejan mediante variables de entorno
- ✅ **Automatización completa**: Ngrok integrado con script personalizado para exponer tu bot local a internet
- ✅ **Testing incluido**: Suite completa de tests unitarios con Docker
- ✅ **Documentación detallada**: Guías paso a paso para configuración y troubleshooting

## 📁 Estructura del Proyecto

```
whatsapp-bot-colombiano/
├── src/                    # Código fuente principal
│   ├── bot/               # Lógica del bot (personalidad, respuestas)
│   ├── services/          # Servicios externos (Twilio)
│   ├── config/            # Configuración (settings.py)
│   └── web/              # Aplicación web (Flask app)
├── tests/                 # Tests unitarios completos
├── docker-compose.yml    # Orquestación de todos los servicios
├── Dockerfile           # Imagen Docker del bot
├── setup.py            # Configuración del paquete Python
├── requirements.txt    # Dependencias de Python
├── .env.example        # Ejemplo de variables de entorno
├── .env               # Tus credenciales (NO subir a Git)
├── LICENSE            # Licencia MIT
├── start_ngrok.sh     # Script de inicio personalizado para Ngrok
└── README.md          # Esta documentación
```

## 🚀 Configuración Rápida

### Prerrequisitos
- **Docker y Docker Compose** instalados en tu sistema
- Cuenta en **[Twilio](https://twilio.com)** con WhatsApp Sandbox habilitado
- Token gratuito de **[Ngrok](https://ngrok.com)** (solo necesitas registrarte)

### Paso 1: Clonar y Configurar el Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/CodeWithBotinaOficial/whatsapp-bot-colombiano.git
cd whatsapp-bot-colombiano

# Copiar la configuración de ejemplo
cp .env.example .env
```

### Paso 2: Configurar Variables de Entorno - PASO CRÍTICO ⚠️

**Edita cuidadosamente** el archivo `.env` con tus credenciales reales. Cada variable es importante:

```env
# ==================== CONFIGURACIÓN DE TWILIO ====================
# Obtén estas credenciales desde https://console.twilio.com
TWILIO_ACCOUNT_SID=your_account_sid_here           # Ej: ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token_here             # Ej: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886       # ¡CÁMBIALO! Usa el número que Twilio te asigne en el Sandbox

# ==================== CONFIGURACIÓN DE NGROK ====================
# Obtén tu token en https://dashboard.ngrok.com/get-started/your-authtoken
NGROK_AUTH_TOKEN=your_ngrok_authtoken_here         # Ej: 2abc3def4ghi5jkl6mno7pqr8stu9vwx
# DOMINIO OPCIONAL - Solo si tienes un subdominio personalizado de Ngrok
# NGROK_DOMAIN=your-custom-subdomain.ngrok-free.app # Si no tienes, déjalo vacío o elimina esta línea

# ==================== CONFIGURACIÓN DE LA APLICACIÓN ====================
# ¡IMPORTANTE! Genera una SECRET_KEY segura con el comando más abajo
SECRET_KEY=your-secret-key-here                    # ¡NO uses este valor! Genera uno nuevo
FLASK_ENV=production
LOG_LEVEL=INFO

# ==================== CONFIGURACIÓN DEL BOT ====================
BOT_NAME=Deep
BOT_PERSONALITY=colombian
```

#### 🔐 Generando tu SECRET_KEY (OBLIGATORIO)

**No uses el valor por defecto `your-secret-key-here`**. Genera una clave segura ejecutando:

```bash
# En Linux/Mac:
python3 -c "import secrets; print(secrets.token_hex(32))"

# En Windows:
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia el resultado (64 caracteres hexadecimales) y pégala como valor de `SECRET_KEY` en tu archivo `.env`.

### Paso 3: Construir e Iniciar con Docker Compose

```bash
# Construir las imágenes y levantar todos los servicios
docker compose up --build

# Para ejecutar en segundo plano (recomendado para uso continuo)
docker compose up -d
```

### Paso 4: Verificar que Todo Funcione ✅

```bash
# Verificar el estado de los contenedores
docker compose ps

# Ver logs del bot (deberías ver "Running on http://0.0.0.0:5000")
docker compose logs whatsapp-bot --tail=10

# Ver logs de Ngrok (deberías ver tu URL pública)
docker compose logs ngrok --tail=15
```

### Paso 5: Configurar el Webhook de Twilio

1. **Ve a la [Consola de Twilio](https://console.twilio.com)**
2. Navega a **Messaging → Try it out → Send a WhatsApp message**
3. En la sección **Sandbox**, busca el campo **"WHEN A MESSAGE COMES IN"**
4. Pega tu **URL de Ngrok** (la que aparece en los logs) seguida de `/webhook`:
   ```
   https://TU-DOMINIO-NGROK.ngrok-free.app/webhook
   ```
5. **Guarda los cambios**

### Paso 6: ¡Probar el Bot! 🎉

Envía un mensaje de WhatsApp al **número de Sandbox de Twilio**:

- **"Hola"** → Saludo colombiano como "¡Quiubo parce!"
- **"¿Qué significa parce?"** → Explicación de la jerga colombiana
- **"Ayuda"** → Menú de comandos disponibles
- **"Chao"** → Despedida con estilo colombiano

## 🐳 Servicios Docker

| Servicio | Puerto | Descripción | Estado Esperado |
|----------|--------|-------------|-----------------|
| `whatsapp-bot` | 5000 | Bot principal (Flask) | `Running` |
| `ngrok-tunnel` | 4040 | Túnel público a internet (con script personalizado) | `Running` (y mostrando URL) |
| `whatsapp-bot-tests` | - | Ejecutor de tests | Solo se ejecuta al correr tests |

**Interfaz web de Ngrok**: Accede a `http://localhost:4040` para ver el tráfico en tiempo real.

## 🔧 Desarrollo y Testing

### Ejecutar Tests Unitarios

```bash
# Ejecutar todos los tests con cobertura
docker compose run --rm tests

# O ejecutar tests específicos
docker compose run --rm tests pytest tests/test_bot.py::TestColombianPersonality -v
```

### Modificar la Personalidad Colombiana

Edita `src/bot/personality.py` para personalizar:

```python
# Ejemplo: Agregar nuevos saludos
GREETINGS: List[str] = [
    "¡Nuevo saludo colombiano!",
    "¿Qué más, mi llave?",
    # ... tus saludos aquí
]

# Ejemplo: Agregar nueva jerga
SLANG: Dict[str, str] = {
    'parcero': 'amigo cercano',
    'guachafita': 'diversión, alboroto',
    # ... tu jerga aquí
}
```

### Agregar Nuevos Comandos

1. Crea una nueva clase en `src/bot/response_handler.py` heredando de `ResponseStrategy`
2. Implementa los métodos `can_handle()` y `get_response()`
3. Agrega la estrategia a la lista en `ResponseHandler.__init__()`

## 🐛 Solución de Problemas

### Problemas Comunes y Soluciones

| Problema | Causa Probable | Solución |
|----------|---------------|----------|
| **Ngrok no se conecta** | Token inválido o expirado | Verifica tu `NGROK_AUTH_TOKEN` en https://dashboard.ngrok.com/get-started/your-authtoken |
| **Error: `ModuleNotFoundError: No module named 'pydantic_settings'`** | Dependencias no instaladas | Ejecuta `docker compose build --no-cache whatsapp-bot` |
| **Error: `secret_key Field required`** | `SECRET_KEY` no configurada | Genera una nueva con el comando de arriba y agrega al `.env` |
| **Twilio no envía mensajes** | Webhook mal configurado | Verifica que la URL en Twilio sea `https://TU-DOMINIO.ngrok-free.app/webhook` |
| **Bot no responde** | Servicio no corriendo | Verifica con `docker compose ps` y `docker compose logs whatsapp-bot` |
| **Contenedores en estado `Restarting`** | Error en configuración | Revisa logs completos: `docker compose logs --tail=50` |
| **Ngrok error: `authentication failed`** | Token no pasado correctamente | Asegúrate de que el script `start_ngrok.sh` esté correctamente configurado |

### Verificar Estado del Sistema

```bash
# Ver estado de todos los contenedores
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Ver logs específicos con detalles
docker compose logs whatsapp-bot --tail=50
docker compose logs ngrok --tail=30

# Probar que el bot responde internamente
curl http://localhost:5000/health
```

### Si los Problemas Persisten

1. **Limpiar todo y empezar de nuevo:**
   ```bash
   docker compose down -v
   docker system prune -a --volumes
   docker compose build --no-cache
   docker compose up -d
   ```

2. **Verificar que las variables de entorno sean correctas:**
   ```bash
   docker compose exec whatsapp-bot printenv | grep -E "(TWILIO|NGROK|SECRET)"
   ```

## 🔒 Seguridad Importante

- **NUNCA subas tu archivo `.env` a GitHub** (está en `.gitignore`)
- **Regenera tu `SECRET_KEY`** si la compartiste accidentalmente
- **Usa diferentes credenciales** para desarrollo y producción
- **Revoca tus tokens de Ngrok/API** si los expusiste
- **El archivo `start_ngrok.sh` contiene lógica sensible** - no lo modifiques a menos que sepas lo que haces

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver el archivo [LICENSE](LICENSE) para más detalles.

Copyright © 2025 CodeWithBotinaOficial

## 🤝 Contribuir

¡Contribuciones son bienvenidas! Para contribuir:

1. Haz fork del proyecto
2. Crea una rama: `git checkout -b feature/mi-nueva-funcionalidad`
3. Commit tus cambios: `git commit -am 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/mi-nueva-funcionalidad`
5. Abre un Pull Request

## 🙏 Agradecimientos

- [Twilio](https://twilio.com) por la API de WhatsApp
- [Ngrok](https://ngrok.com) por el tunneling gratuito
- La rica cultura colombiana por la inspiración 🇨🇴
- A todos los contribuyentes y testers del proyecto

---

**¿Preguntas o problemas?** ¡Abre un issue en GitHub o únete a nuestras discusiones!

**¡Listo para conectar!** Una vez configurado, tu bot estará recibiendo mensajes con toda la actitud colombiana. 🎉