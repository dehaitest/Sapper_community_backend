import json
import re
from decouple import config
from app.services.LLMs.Chatgpt import Chatgpt
import asyncio
import os

class GetLLMResponse:
    def __init__(self, process) -> None:
        self.process = process

    async def get_LLM_Response(self, prompt):
        try:
            async for part in self.process(prompt):
                yield part
        except Exception as e:
            # 处理异常，例如记录日志或返回错误消息
            print(f"Error in LLM response: {e}")

# 使用示例
# 从环境变量或配置文件中获取API密钥
# api_key = config("OPENAI_KEY")
# if not api_key:
#     raise ValueError("OPENAI_KEY")
#
# chat_service = Chatgpt(api_key)
# require2SPLForm_instance = GetLLMResponse(chat_service.process_message)
#
# # 异步调用示例
# async def main():
#     message = [{"role": "user", "content": "How are you"}]
#     async for response_part in require2SPLForm_instance.get_LLM_Response(message):
#         print(response_part)
#
# # 运行主程序
# if __name__ == "__main__":
#     asyncio.run(main())
