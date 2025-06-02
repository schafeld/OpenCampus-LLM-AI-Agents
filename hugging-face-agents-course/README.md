# Hugging Face Agents Course

This [course](https://huggingface.co/learn/agents-course/) is part of / homework for [EduHub's "From LLMs to AI Agents"](https://edu.opencampus.sh/course/563) course. [HuggingFAce agents-course repository](https://github.com/huggingface/agents-course).

## Notes

### Unit 0 Welcome

[Onboarding](https://huggingface.co/learn/agents-course/unit0/onboarding)

Pull Ollama model:

```bash
ollama pull qwen2:7b
```

Use `LiteLLMModel` instead of `InferenceClientModel`

```bash
pip install 'smolagents[litellm]'
```

Check if Ollama server is running:

bash```
http://localhost:11434
```

