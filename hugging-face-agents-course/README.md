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

```bash
open http://localhost:11434
```

Use [Anaconda](https://www.anaconda.com/download) Jupyter Lab to access local copy of [course Jupyter Lab](https://huggingface.co/agents-course/notebooks/blob/main/unit1/dummy_agent_library.ipynb).

Set Hugging Face Access token (with saved Git credentials):

```bash
huggingface-cli login --add-to-git-credential --token  <YOUR_HUGGINGFACE_TOKEN>
```

The token is saved to `~/.cache/huggingface/stored_tokens`.
