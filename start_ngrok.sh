#!/bin/sh

echo "⏳ Esperando 5 segundos para asegurar que Flask esté listo..."
sleep 5

BASE_CMD="ngrok http whatsapp-bot:5000 --authtoken=${NGROK_AUTH_TOKEN}"

if [ -n "$NGROK_DOMAIN" ]; then
    echo "✅ Usando dominio personalizado: $NGROK_DOMAIN"
    exec $BASE_CMD --domain="$NGROK_DOMAIN"
else
    echo "ℹ️ Sin dominio personalizado. Ngrok asignará uno aleatorio."
    exec $BASE_CMD
fi