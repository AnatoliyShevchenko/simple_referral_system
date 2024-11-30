#!/bin/bash

# Проверка, что все необходимые параметры переданы
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <host> <port> <timeout>"
    exit 1
fi

HOST=$1
PORT=$2
TIMEOUT=$3

# Функция для проверки доступности порта
check_port() {
    nc -z "$HOST" "$PORT" > /dev/null 2>&1
}

# Основной цикл ожидания
elapsed=0
while ! check_port; do
    if [ $elapsed -ge $TIMEOUT ]; then
        echo "Timeout reached. $HOST:$PORT is not available."
        exit 1
    fi
    echo "Waiting for $HOST:$PORT to become available..."
    sleep 1
    elapsed=$((elapsed + 1))
done

echo "$HOST:$PORT is now available."
