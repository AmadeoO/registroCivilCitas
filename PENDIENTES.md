# Pendientes

## 1. Añadir secrets en GitHub (URGENTE - sin esto GitHub Actions no funciona)

Ir a: https://github.com/AmadeoO/registroCivilCitas/settings/secrets/actions

Crear estos dos secrets:

| Name | Secret |
|---|---|
| `TELEGRAM_BOT_TOKEN` | `8990112574:AAFzrr460GFS1v5Lm5C9ef3HPtWx_1W1nxQ` |
| `TELEGRAM_CHAT_ID` | `-5596546259` |

---

## 2. Probar ejecución manual en GitHub Actions

Una vez añadidos los secrets:
- Ir a: https://github.com/AmadeoO/registroCivilCitas/actions
- Seleccionar el workflow "Verificador de Citas"
- Clic en "Run workflow" → "Run workflow"
- Verificar que llega notificación al grupo de Telegram

---

## 3. Revocar tokens de GitHub usados en el chat (seguridad)

Ir a: https://github.com/settings/tokens
Revocar estos tokens que quedaron expuestos en la conversación:
- github_pat_11AHNZ5EI0zY88WohM94Aa_...
- github_pat_11AHNZ5EI0WOyYlW2t1YmH_...
- github_pat_11AHNZ5EI01YMCWt7jYJF0_...

---

## 4. Revocar token del bot de Telegram (seguridad)

El token del bot también quedó expuesto en el chat.
- Abrir Telegram → @BotFather → /mybots → seleccionar el bot → API Token → Revoke
- Actualizar el nuevo token en:
  - GitHub Secret: TELEGRAM_BOT_TOKEN
  - scripts/config.py (local)

---

## 5. Ajuste de horarios por zona horaria (opcional)

El workflow de GitHub Actions usa UTC. España está en UTC+2 (verano) / UTC+1 (invierno).
Archivo: .github/workflows/check_citas.yml

Horarios actuales configurados (UTC):
- 02:00 UTC = 04:00 España (verano)
- 06:00 UTC = 08:00 España (verano)
- 14:00 UTC = 16:00 España (verano)
- 18:00 UTC = 20:00 España (verano)

En invierno habrá 1 hora de desfase. Ajustar si es necesario.
