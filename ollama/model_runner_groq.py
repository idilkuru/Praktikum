# model_runner.py
def query_llm_groq(prompt: str, model="qwen1.5-7b-chat", api_key=None) -> str:
    import openai
    openai.api_key = api_key or os.getenv("GROQ_API_KEY")

    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
