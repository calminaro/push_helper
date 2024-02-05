# Push Helper

Semplice helper per notifiche push usando Mail e Telegram

### Esempio

```bash
#!/bin/bash

BCK_SRC="SOURCE_DIR"
BCK_RCLONE="RCLONE_DIR"

rclone dedupe --dedupe-mode newest rclone dedupe --dedupe-mode newest

if [[ $? -eq 0 ]]
then
    echo "BACKUP ELIMINATI DUPLICATI"
else
    python3 bot.py "rclone dedupe" "ERRORE"
fi

rclone sync -P $BCK_SRC $BCK_RCLONE

if [[ $? -eq 0 ]]
then
    echo "BACKUP CLOUD OK"
else
    python3 bot.py "rclone sync" "ERRORE"
fi

```

Nell'esempio se il backup non va a buon fine invia un messaggio per avvertire l'utente formattato:

```textile
rclone sync: ERRORE
```
