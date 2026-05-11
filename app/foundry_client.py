"""
Wrapper around the Azure OpenAI / Foundry chat completions API.
Keeps conversation history so the chatbot has memory across turns.
"""
from openai import AzureOpenAI


class FoundryChatClient:
    def __init__(self, endpoint: str, api_key: str, deployment: str,
                 api_version: str, system_prompt: str):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self.deployment = deployment
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def reset(self):
        """Clear conversation history but keep the system prompt."""
        self.history = [{"role": "system", "content": self.system_prompt}]

    def send_message(self, user_message: str, temperature: float = 0.7,
                     max_tokens: int = 800) -> str:
        """Send a user message and return the assistant's reply."""
        self.history.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=self.history,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply
