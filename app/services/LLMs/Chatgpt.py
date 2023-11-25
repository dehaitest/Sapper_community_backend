import openai
import asyncio

class Chatgpt():
    def __init__(self, api_key) -> None:
        openai.api_key = api_key
        self.stream = True

    async def process_message(self, message: str):
        for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
                stream=True
        ):
            if response.choices[0]["finish_reason"] == "stop":
                yield "__END_OF_RESPONSE__"
                break
            await asyncio.sleep(0.001)
            yield response['choices'][0]['delta']['content']
