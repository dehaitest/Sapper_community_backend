import asyncio
import websockets

async def websocket_client(uri, message, client_id):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)

        print(f"Client {client_id} received:")
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                print(f"\nClient {client_id} completed.\n")
                break
            else:
                print(f"{response}")
        # Explicitly close the connection
        await websocket.close()
        print(f"Client {client_id} connection closed.")

async def requiretosplform():
    uri = "ws://localhost:8000/ws/sapperchain/requiretosplform"
    # uri = "wss://v1.promptsapper.tech/ws/sapperchain/requiretosplform"
    message = "High school math tutor to help students solve math problems and provide detailed instruction."
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def splformtonl():
    uri = "ws://localhost:8000/ws/sapperchain/splformtonl"
    # uri = "wss://v1.promptsapper.tech/ws/sapperchain/splformtonl"
    async with websockets.connect(uri) as websocket:
        message = '''{"id": 1, "name": "test", "image": "", "spl": "{\\\"Persona\\\": {\\\"Description-0\\\": \\\"An excellent high school mathematics tutor.\\\"}, \\\"Audience\\\": {\\\"Description-0\\\": \\\"High school students with poor math scores.\\\"}, \\\"Terminology\\\": {\\\"Description-0\\\": \\\"Algebra\\\", \\\"Description-1\\\": \\\"Geometry\\\", \\\"Description-2\\\": \\\"Statistics\\\"}, \\\"ContextControl\\\": {\\\"Rule-0\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\", \\\"Rule-1\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\", \\\"Rule-2\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}, \\\"Instruction-0\\\": {\\\"Name\\\": \\\"Analyze problem\\\", \\\"Commands\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"], \\\"Rules\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}, \\\"Instruction-1\\\": {\\\"Name\\\": \\\"Provide guidance\\\", \\\"Commands\\\": [\\\"Break down the problem into smaller, manageable steps.\\\", \\\"Provide clear and detailed explanations for each step.\\\", \\\"Encourage the student to ask questions and seek clarification when necessary.\\\"], \\\"Rules\\\": [\\\"Avoid complex mathematical jargon that may further confuse the student.\\\", \\\"Ensure that the step-by-step guidance is tailored to the student's current understanding of the subject.\\\"]}}", "spl_form": "{\\\"formData\\\": [{\\\"sectionId\\\": \\\"0\\\", \\\"sectionType\\\": \\\"Persona\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"An excellent high school mathematics tutor.\\\"}]}, {\\\"sectionId\\\": \\\"1\\\", \\\"sectionType\\\": \\\"Audience\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"High school students with poor math scores.\\\"}]}, {\\\"sectionId\\\": \\\"2\\\", \\\"sectionType\\\": \\\"Terminology\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Algebra\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Description-1\\\", \\\"content\\\": \\\"Geometry\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Description-2\\\", \\\"content\\\": \\\"Statistics\\\"}]}, {\\\"sectionId\\\": \\\"3\\\", \\\"sectionType\\\": \\\"ContextControl\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Rule-0\\\", \\\"content\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Rule-1\\\", \\\"content\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rule-2\\\", \\\"content\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}]}, {\\\"sectionId\\\": \\\"4\\\", \\\"sectionType\\\": \\\"Instruction-0\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Analyze problem\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}]}, {\\\"sectionId\\\": \\\"5\\\", \\\"sectionType\\\": \\\"Instruction-1\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Provide guidance\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Break down the problem into smaller, manageable steps.\\\", \\\"Provide clear and detailed explanations for each step.\\\", \\\"Encourage the student to ask questions and seek clarification when necessary.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid complex mathematical jargon that may further confuse the student.\\\", \\\"Ensure that the step-by-step guidance is tailored to the student's current understanding of the subject.\\\"]}]}]}", "nl": "", "created_by": "sapper", "create_datetime": "2023-11-30T06:53:04", "update_datetime": "2023-11-30T06:53:04", "active": true}'''
        await websocket.send(message)
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def notosplform():
    uri = "ws://localhost:8000/ws/sapperchain/nltosplform"
    # uri = "wss://v1.promptsapper.tech/ws/sapperchain/nltosplform"
    async with websockets.connect(uri) as websocket:
        message = '''{"id": 1, "name": "test", "image": "", "spl": "{\\\"Persona\\\": {\\\"Description-0\\\": \\\"An excellent high school mathematics tutor.\\\"}, \\\"Audience\\\": {\\\"Description-0\\\": \\\"High school students with poor math scores.\\\"}, \\\"Terminology\\\": {\\\"Description-0\\\": \\\"Algebra\\\", \\\"Description-1\\\": \\\"Geometry\\\", \\\"Description-2\\\": \\\"Statistics\\\"}, \\\"ContextControl\\\": {\\\"Rule-0\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\", \\\"Rule-1\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\", \\\"Rule-2\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}, \\\"Instruction-0\\\": {\\\"Name\\\": \\\"Analyze problem\\\", \\\"Commands\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"], \\\"Rules\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}, \\\"Instruction-1\\\": {\\\"Name\\\": \\\"Provide guidance\\\", \\\"Commands\\\": [\\\"Break down the problem into smaller, manageable steps.\\\", \\\"Provide clear and detailed explanations for each step.\\\", \\\"Encourage the student to ask questions and seek clarification when necessary.\\\"], \\\"Rules\\\": [\\\"Avoid complex mathematical jargon that may further confuse the student.\\\", \\\"Ensure that the step-by-step guidance is tailored to the student's current understanding of the subject.\\\"]}}", "spl_form": "{\\\"formData\\\": [{\\\"sectionId\\\": \\\"0\\\", \\\"sectionType\\\": \\\"Persona\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"An excellent high school mathematics tutor.\\\"}]}, {\\\"sectionId\\\": \\\"1\\\", \\\"sectionType\\\": \\\"Audience\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"High school students with poor math scores.\\\"}]}, {\\\"sectionId\\\": \\\"2\\\", \\\"sectionType\\\": \\\"Terminology\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Algebra\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Description-1\\\", \\\"content\\\": \\\"Geometry\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Description-2\\\", \\\"content\\\": \\\"Statistics\\\"}]}, {\\\"sectionId\\\": \\\"3\\\", \\\"sectionType\\\": \\\"ContextControl\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Rule-0\\\", \\\"content\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Rule-1\\\", \\\"content\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rule-2\\\", \\\"content\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}]}, {\\\"sectionId\\\": \\\"4\\\", \\\"sectionType\\\": \\\"Instruction-0\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Analyze problem\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}]}, {\\\"sectionId\\\": \\\"5\\\", \\\"sectionType\\\": \\\"Instruction-1\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Provide guidance\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Break down the problem into smaller, manageable steps.\\\", \\\"Provide clear and detailed explanations for each step.\\\", \\\"Encourage the student to ask questions and seek clarification when necessary.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid complex mathematical jargon that may further confuse the student.\\\", \\\"Ensure that the step-by-step guidance is tailored to the student's current understanding of the subject.\\\"]}]}]}", "nl": "{\\\"NL\\\": [{\\\"id\\\": 0, \\\"type\\\": [\\\"Persona\\\", \\\"Terminology\\\"], \\\"content\\\": \\\"The persona is an excellent high school mathematics tutor, specialized in areas such as algebra, geometry, and statistics.\\\"}, {\\\"id\\\": 1, \\\"type\\\": [\\\"Audience\\\"], \\\"content\\\": \\\"The primary audience for this tutor is high school students who are good at statistic.\\\"}, {\\\"id\\\": 2, \\\"type\\\": [\\\"ContextControl\\\"], \\\"content\\\": \\\"The context control includes using clear and concise explanations, avoiding unnecessary jargon, guiding students through the problem-solving process step by step while emphasizing logic and reasoning, and tailoring teaching strategies to cater to individual needs and provide personalized assistance.\\\"}, {\\\"id\\\": 3, \\\"type\\\": [\\\"Instruction\\\"], \\\"content\\\": \\\"The instructions for analyzing the problem involve reading and understanding the problem statement together with the student, identifying the key information and any given conditions or constraints, discussing and clarifying any unfamiliar terms or symbols, and determining the specific mathematical concepts and skills required to solve the problem. Additionally, the rules stress on avoiding overly complex or ambiguous phrasing and providing appropriate explanations or mathematical concepts to facilitate user understanding.\\\"}, {\\\"id\\\": 4, \\\"type\\\": [\\\"Instruction\\\"], \\\"content\\\": \\\"The instructions for providing guidance include breaking down the problem into smaller, manageable steps, providing clear and detailed explanations for each step, and encouraging the student to ask questions and seek clarification when necessary. Moreover, the rules emphasize avoiding complex mathematical jargon that may confuse the student and ensuring that the step-by-step guidance is tailored to the student's current understanding of the subject.\\\"}]}", "created_by": "sapper", "create_datetime": "2023-11-30T07:12:08", "update_datetime": "2023-11-30T07:12:37", "active": true}'''
        await websocket.send(message)
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def main():
    # uri = "wss://v1.promptsapper.tech/ws/sapperchain/requiretosplform"
    # uri = "ws://localhost:8000/ws/sapperchain/requiretosplform"

    # message = "High school math tutor to help students solve math problems and provide detailed instruction."
    # client_count = 1  # Number of concurrent clients

    # tasks = [websocket_client(uri, message, i) for i in range(client_count)]
    # await asyncio.gather(*tasks)

    # uri = "ws://localhost:8000/ws/sapperchain/requiretosplform"
    # client_count = 1  # Number of concurrent clients

    # tasks = [websocket_client(uri, message, i) for i in range(client_count)]
    # await asyncio.gather(*tasks)

    while True:
        test_index = input("Test index: ")
        if test_index == "1":
            await requiretosplform() 
        elif test_index == "2":
            await splformtonl() 
        elif test_index == "3":
            await notosplform() 
        else: 
            break


if __name__ == "__main__":
    asyncio.run(main())
