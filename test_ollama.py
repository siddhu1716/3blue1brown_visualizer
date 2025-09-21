import httpx

# Replace with your Ollama server host and port
OLLAMA_URL = "http://192.168.13.162:11434/api/generate"

# Example payload to send to the model
payload = {
    "model": "llama3.1-8b",
    "prompt": "Animate the convergence of the Taylor series for e^x",
    "max_tokens": 100
}

try:
    response = httpx.post(OLLAMA_URL, json=payload)
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
except httpx.RequestError as e:
    print("Error connecting to Ollama:", e)
