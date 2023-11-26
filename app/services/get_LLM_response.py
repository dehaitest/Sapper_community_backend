class GetLLMResponse:
    def __init__(self, process) -> None:
        self.process = process

    async def get_LLM_Response(self, prompt):
        try:
            async for part in self.process(prompt):
                yield part
        except Exception as e:
            print(f"Error in LLM response: {e}")


