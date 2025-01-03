export OLLAMA_DOMAIN=localhost
export OLLAMA_PORT=5000
export OLLAMA_HOST=$OLLAMA_DOMAIN:$OLLAMA_PORT

ollama serve
ollama run sai:latest