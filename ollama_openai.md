# Ollama OpenAI-Compatible API Reference
### Maintained for **Saathi AI** by **Pratham Prasad**

Ollama provides an OpenAI-compatible `/v1` endpoint. This allows Saathi AI to integrate with any OpenAI-compatible client library while maintaining 100% on-device local execution.

---

## 1. Endpoint Configuration

- **Base URL**: `http://127.0.0.1:11434/v1`
- **Authentication**: Bearer token (arbitrary string or `ollama` when local):
  ```http
  Authorization: Bearer ollama
  ```

---

## 2. Chat Completions (`POST /v1/chat/completions`)

### Request Payload:
```json
{
  "model": "qwen2.5:7b",
  "messages": [
    {
      "role": "system",
      "content": "You are Saathi, an ultra-advanced cognitive co-pilot created by Pratham Prasad."
    },
    {
      "role": "user",
      "content": "List the files in my Projects folder."
    }
  ],
  "temperature": 0.3,
  "stream": false
}
```

---

## 3. Function & Tool Calling Integration

Ollama supports OpenAI-standard `tools` definitions:

```json
{
  "model": "qwen2.5:7b",
  "messages": [...],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "create_file",
        "description": "Create a file at target path with specified content",
        "parameters": {
          "type": "object",
          "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"}
          },
          "required": ["path", "content"]
        }
      }
    }
  ]
}
```

---

## 4. Models Discovery (`GET /v1/models`)

Returns an array of locally pulled Ollama models available for inference:
```bash
curl http://127.0.0.1:11434/v1/models
```