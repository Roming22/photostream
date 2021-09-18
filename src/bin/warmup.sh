#!/bin/bash -e
SCRIPT_DIR="$(cd "$(dirname "$0")"; pwd)"

get_url(){
}
start_server(){
    "$SCRIPT_DIR/server.sh" &
    SERVER_PID="$!"
}

warmup_server(){
    URL_PREFIX="http://localhost:8000"
    while ! curl -o /dev/null -s "${URL_PREFIX}"; do
        sleep 1
    done
    for URL_SUFFIX in  /unittest /unittest/random; do
        URL="${URL_PREFIX}/${URL_SUFFIX}"
        curl -o /dev/null -s $URL && echo "$URL: OK" || echo "$URL: FAIL"
    done
}

stop_server(){
    kill -9 $SERVER_PID
}

start_server
warmup_server
stop_server