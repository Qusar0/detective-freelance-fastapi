#!/bin/sh

# Проверка переменных
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$DB_NAME" ]; then
  echo "ERROR: Missing required environment variables" >&2
  exit 1
fi

export TZ=Europe/Moscow
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/backups/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "Creating backup of ${DB_NAME} from ${DB_HOST}:${DB_PORT} at $(date)"

# Явно указываем подключение через TCP
PGPASSWORD="${DB_PASS}" pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" | gzip > "${BACKUP_FILE}"

# Проверка успешности бэкапа
if [ $? -ne 0 ]; then
  echo "Backup FAILED" >&2
  rm -f "${BACKUP_FILE}"
  exit 1
fi

# Удаление старых бэкапов
ls -1t /backups/backup_${DB_NAME}_*.sql.gz | tail -n +8 | xargs rm -f

echo "Backup completed: ${BACKUP_FILE}"