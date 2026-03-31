# Despliegue con Nginx + Systemd para Gestion Mantenimiento

Este es un ejemplo completo de configuración para desplegar la app Django en un servidor Linux (ej. Ubuntu) usando Nginx como proxy inverso y Systemd para gestionar el proceso de Gunicorn.

## Requisitos Previos
- Servidor VPS (ej. DigitalOcean, AWS EC2) con Ubuntu/Debian.
- Python 3.9+, virtualenv, pip.
- Nginx y Gunicorn instalados: `sudo apt update && sudo apt install nginx python3-gunicorn`.
- Proyecto clonado en el servidor.

## Pasos de Configuración

### 1. Preparar el Proyecto
- Clona el repo: `git clone <tu-repo> /ruta/a/tu/proyecto`
- Crea virtualenv: `python3 -m venv /ruta/a/tu/venv`
- Activa: `source /ruta/a/tu/venv/bin/activate`
- Instala dependencias: `pip install -r requirements.txt` (agrega `gunicorn` si no está).
- Ejecuta migraciones: `python manage.py migrate`
- Recoge static: `python manage.py collectstatic`
- Configura `settings.py` para producción: `DEBUG = False`, `ALLOWED_HOSTS = ['tu-dominio.com']`, usa variables de entorno para secrets.

### 2. Configurar Systemd
- Copia `systemd.service` a `/etc/systemd/system/gestion_mantenimiento.service`
- Edita las rutas: `/ruta/a/tu/proyecto`, `/ruta/a/tu/venv`, `tu-usuario`.
- Habilita e inicia: `sudo systemctl enable gestion_mantenimiento && sudo systemctl start gestion_mantenimiento`
- Verifica: `sudo systemctl status gestion_mantenimiento`

### 3. Configurar Nginx
- Copia `nginx.conf` a `/etc/nginx/sites-available/gestion_mantenimiento`
- Edita rutas: `/ruta/a/tu/proyecto`, `tu-dominio.com`.
- Habilita sitio: `sudo ln -s /etc/nginx/sites-available/gestion_mantenimiento /etc/nginx/sites-enabled/`
- Prueba config: `sudo nginx -t`
- Reinicia: `sudo systemctl reload nginx`

### 4. Configurar Firewall y SSL
- Abre puerto 80/443: `sudo ufw allow 80 && sudo ufw allow 443`
- Instala Certbot para SSL: `sudo apt install certbot python3-certbot-nginx`
- Obtén certificado: `sudo certbot --nginx -d tu-dominio.com`

## Troubleshooting
- Logs de app: `sudo journalctl -u gestion_mantenimiento`
- Logs de Nginx: `sudo tail -f /var/log/nginx/error.log`
- Si no carga, verifica permisos de socket y staticfiles.
- Para reinicio completo: `sudo systemctl restart gestion_mantenimiento && sudo systemctl reload nginx`

## Notas
- Cambia todas las rutas por las reales en tu servidor.
- Para gratis, usa Railway en lugar de VPS (más simple).
- Si usas base de datos externa (no SQLite), configura en settings.py.