data_path = "./data.csv"

query_times = 1

start_text = "您好，这里是长江时代客服中心，很高兴为您服务。请问有什么可以帮到您的吗？"

PORT = 8765
# Redis配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 5

# 外部接口
model_name = "qwen-api" # LLM
ASR_URL = "http://81.69.253.47:5000/transcribe/file"
ASR_WEBSOCKET_HOST = 'localhost:10095'
TTS_URL = "http://127.0.0.1:8910/tts_stream"