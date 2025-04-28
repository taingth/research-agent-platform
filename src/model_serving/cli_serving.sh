choice_framework=$1

if [ "$choice_framework" = "vllm" ]; then
    echo "Starting vLLM framework..."
    uv run python -m vllm.entrypoints.openai.api_server --model Qwen/QwQ-32B-AWQ --enable-reasoning --reasoning-parser deepseek_r1 --enable-auto-tool-choice --tool-call-parser hermes --tensor-parallel-size 2 --max-model-len 8000 --gpu-memory-utilization 0.8 --enforce-eager --port 3001
elif [ "$choice_framework" = "sglang" ]; then
    echo "Starting SGLang framework..."
    uv run python -m sglang.launch_server --model-path Qwen/QwQ-32B-AWQ --tp 2 --mem-fraction-static 0.8 --enable-torch-compile --tool-call-parser qwen25 --reasoning-parser deepseek-r1 --port 3001 --host 0.0.0.0 --attention-backend flashinfer
else
    echo "Usage: $0 [vllm|sglang]"
    echo "  vllm    - Start the vLLM framework"
    echo "  sglang  - Start the SGLang framework"
    exit 1
fi