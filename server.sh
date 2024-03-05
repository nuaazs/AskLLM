#!/bin/bash

PYTHONPATH=./
export CUDA_VISIBLE_DEVICES=6
GUNICORN_PORT=8765
APP_NAME="main:app"
GUNICORN_PID_FILE="log/gunicorn.pid"
LOG_FILE="log/chatbot_service.log"

# TTS
TTS_PIF_FILE="log/tts_server_gunicorn.pid"
TTS_LOG_FILE="log/tts_service.log"

start() {
    echo "Starting TTS server..."
    now_path=$(pwd)
    cd /datasets_ssd/models/badXT-GPT-SoVITS/GPT-SoVITS/GPT_SoVITS
    CUDA_VISIBLE_DEVICES=6 nohup gunicorn -w 1 -b 0.0.0.0:8911 app:app --daemon --pid ${TTS_PIF_FILE} --access-logfile ${TTS_LOG_FILE} --error-logfile ${TTS_LOG_FILE} >> ${TTS_LOG_FILE} 2>&1
    cd ${now_path}
    echo "Starting chatbot server..."
    CUDA_VISIBLE_DEVICES=6 gunicorn -w 1 -b 0.0.0.0:${GUNICORN_PORT} ${APP_NAME} --daemon --pid ${GUNICORN_PID_FILE} --access-logfile ${LOG_FILE} --error-logfile ${LOG_FILE}
    echo "Chatbot server started."

    echo "Starting chatbot DEMO..."
    cd examples
    nohup python3 app.py >> ${LOG_FILE} 2>&1 &
    cd ../
    echo $! > ./chatbot_demo.pid
    echo "Chatbot DEMO started."
}

stop() {
    echo "Stopping TTS server..."
    if [ -f ${TTS_PIF_FILE} ]; then
        kill -9 $(cat ${TTS_PIF_FILE})
        rm ${TTS_PIF_FILE}
    else
        echo "TTS server PID file not found. Is the server running?"
    fi

    echo "Stopping chatbot server..."
    if [ -f ${GUNICORN_PID_FILE} ]; then
        kill -9 $(cat ${GUNICORN_PID_FILE})
        rm ${GUNICORN_PID_FILE}
    else
        echo "Chatbot server PID file not found. Is the server running?"
    fi

    echo "Stopping chatbot DEMO..."
    if [ -f ./chatbot_demo.pid ]; then
        kill -9 $(cat ./chatbot_demo.pid)
        rm ./chatbot_demo.pid
    else
        echo "Chatbot DEMO PID file not found. Is the DEMO running?"
    fi
}

restart() {
    stop
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
esac