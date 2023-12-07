# Push Helper

Semplice helper per notifiche push usando Telegram

### Esempio

```bash
#!/bin/bash

BCK_SRC="SOURCE_DIR"
BCK_RCLONE="RCLONE_DIR"

rclone sync -P $BCK_SRC $BCK_RCLONE

if [[ $? -eq 0 ]]
then
 echo "BACKUP CLOUD OK"
else
 python3 bot.py rclone "ERRORE"
fi
```

Nell'esempio se il backup non va a buon fine invia un messaggio per avvertire l'utente formattato:

```textile
rclone: ERRORE
```
