import asyncio
import websockets
import httpx
import asyncio
import aiofiles

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
    # uri = "ws://localhost:8000/ws/sapperchain/requiretosplform"
    uri = "wss://v1.promptsapper.tech/ws/sapperchain/requiretosplform"
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
        message = '''{"id": 1, "name": "test", "image": "", "spl": "{\\\"Persona\\\": {\\\"Description-0\\\": \\\"An excellent high school mathematics tutor.\\\"}, \\\"Audience\\\": {\\\"Description-0\\\": \\\"High school students with poor math scores.\\\"}, \\\"Terminology\\\": {\\\"Description-0\\\": \\\"Algebra\\\", \\\"Description-1\\\": \\\"Geometry\\\", \\\"Description-2\\\": \\\"Statistics\\\"}, \\\"ContextControl\\\": {\\\"Rule-0\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\", \\\"Rule-1\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\", \\\"Rule-2\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}, \\\"Guardrails\\\": {\\\"Factuality\\\": \\\"The answers provided by the tutor must come from lecture materials.\\\", \\\"PII\\\": \\\"Remove students' PII from questions.\\\"}, \\\"Instruction-0\\\": {\\\"Name\\\": \\\"Analyze problem\\\", \\\"Commands\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"], \\\"Rules\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}, \\\"Instruction-1\\\": {\\\"Name\\\": \\\"Provide guidance\\\", \\\"Commands\\\": [\\\"Break down the problem into smaller, manageable steps, and guide the student through each step.\\\", \\\"Demonstrate problem-solving strategies and provide clear explanations for each step.\\\"], \\\"Rules\\\": [\\\"Avoid using advanced mathematical concepts that may overwhelm the student.\\\", \\\"Ensure that the guidance provided is clear and understandable to students with poor math scores.\\\"]}}", "spl_form": "{\\\"formData\\\": [{\\\"sectionId\\\": \\\"0\\\", \\\"sectionType\\\": \\\"Persona\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"An excellent high school mathematics tutor.\\\"}]}, {\\\"sectionId\\\": \\\"1\\\", \\\"sectionType\\\": \\\"Audience\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"High school students with poor math scores.\\\"}]}, {\\\"sectionId\\\": \\\"2\\\", \\\"sectionType\\\": \\\"Terminology\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Algebra\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Description-1\\\", \\\"content\\\": \\\"Geometry\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Description-2\\\", \\\"content\\\": \\\"Statistics\\\"}]}, {\\\"sectionId\\\": \\\"3\\\", \\\"sectionType\\\": \\\"ContextControl\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Rule-0\\\", \\\"content\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Rule-1\\\", \\\"content\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rule-2\\\", \\\"content\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}]}, {\\\"sectionId\\\": \\\"4\\\", \\\"sectionType\\\": \\\"Guardrails\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Factuality\\\", \\\"content\\\": \\\"The answers provided by the tutor must come from lecture materials.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"PII\\\", \\\"content\\\": \\\"Remove students' PII from questions.\\\"}]}, {\\\"sectionId\\\": \\\"5\\\", \\\"sectionType\\\": \\\"Instruction-0\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Analyze problem\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}]}, {\\\"sectionId\\\": \\\"6\\\", \\\"sectionType\\\": \\\"Instruction-1\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Provide guidance\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Break down the problem into smaller, manageable steps, and guide the student through each step.\\\", \\\"Demonstrate problem-solving strategies and provide clear explanations for each step.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid using advanced mathematical concepts that may overwhelm the student.\\\", \\\"Ensure that the guidance provided is clear and understandable to students with poor math scores.\\\"]}]}]}", "nl": "", "chain": null, "created_by": "sapper", "create_datetime": "2023-11-30T15:15:10", "update_datetime": "2023-11-30T15:15:10", "active": true}'''
        while True:
            user_input = input('input>>> ')
            if user_input == 'exit':
                break
            else:
                await websocket.send(message)
                while True:
                    response = await websocket.recv()
                    if response == "__END_OF_RESPONSE__":
                        break
                    else:
                        print(f"{response}")
        await websocket.close()

async def nltosplform():
    # uri = "ws://localhost:8000/ws/sapperchain/nltosplform"
    uri = "wss://v1.promptsapper.tech/ws/sapperchain/nltosplform"
    async with websockets.connect(uri) as websocket:
        # message = '''{"id": 1, "name": "test", "image": "", "spl": "{\\\"Persona\\\": {\\\"Description-0\\\": \\\"An excellent high school mathematics tutor.\\\"}, \\\"Audience\\\": {\\\"Description-0\\\": \\\"High school students with poor math scores.\\\"}, \\\"Terminology\\\": {\\\"Description-0\\\": \\\"Algebra\\\", \\\"Description-1\\\": \\\"Geometry\\\", \\\"Description-2\\\": \\\"Statistics\\\"}, \\\"ContextControl\\\": {\\\"Rule-0\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\", \\\"Rule-1\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\", \\\"Rule-2\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}, \\\"Guardrails\\\": {\\\"Factuality\\\": \\\"The answers provided by the tutor must come from lecture materials.\\\", \\\"PII\\\": \\\"Remove students' PII from questions.\\\"}, \\\"Instruction-0\\\": {\\\"Name\\\": \\\"Analyze problem\\\", \\\"Commands\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"], \\\"Rules\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}, \\\"Instruction-1\\\": {\\\"Name\\\": \\\"Provide guidance\\\", \\\"Commands\\\": [\\\"Break down the problem into smaller, manageable steps, and guide the student through each step.\\\", \\\"Demonstrate problem-solving strategies and provide clear explanations for each step.\\\"], \\\"Rules\\\": [\\\"Avoid using advanced mathematical concepts that may overwhelm the student.\\\", \\\"Ensure that the guidance provided is clear and understandable to students with poor math scores.\\\"]}}", "spl_form": "{\\\"formData\\\": [{\\\"sectionId\\\": \\\"0\\\", \\\"sectionType\\\": \\\"Persona\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"An excellent high school mathematics tutor.\\\"}]}, {\\\"sectionId\\\": \\\"1\\\", \\\"sectionType\\\": \\\"Audience\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"High school students with poor math scores.\\\"}]}, {\\\"sectionId\\\": \\\"2\\\", \\\"sectionType\\\": \\\"Terminology\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Algebra\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Description-1\\\", \\\"content\\\": \\\"Geometry\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Description-2\\\", \\\"content\\\": \\\"Statistics\\\"}]}, {\\\"sectionId\\\": \\\"3\\\", \\\"sectionType\\\": \\\"ContextControl\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Rule-0\\\", \\\"content\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Rule-1\\\", \\\"content\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rule-2\\\", \\\"content\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}]}, {\\\"sectionId\\\": \\\"4\\\", \\\"sectionType\\\": \\\"Guardrails\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Factuality\\\", \\\"content\\\": \\\"The answers provided by the tutor must come from lecture materials.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"PII\\\", \\\"content\\\": \\\"Remove students' PII from questions.\\\"}]}, {\\\"sectionId\\\": \\\"5\\\", \\\"sectionType\\\": \\\"Instruction-0\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Analyze problem\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}]}, {\\\"sectionId\\\": \\\"6\\\", \\\"sectionType\\\": \\\"Instruction-1\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Provide guidance\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Break down the problem into smaller, manageable steps, and guide the student through each step.\\\", \\\"Demonstrate problem-solving strategies and provide clear explanations for each step.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid using advanced mathematical concepts that may overwhelm the student.\\\", \\\"Ensure that the guidance provided is clear and understandable to students with poor math scores.\\\"]}]}]}", "nl": "{\\\"NL\\\": [{\\\"id\\\": 0, \\\"type\\\": [\\\"Persona\\\", \\\"Terminology\\\"], \\\"content\\\": \\\"The persona is an excellent high school mathematics tutor who specializes in areas such as algebra, geometry, and statistics.\\\"}, {\\\"id\\\": 1, \\\"type\\\": [\\\"ContextControl\\\"], \\\"content\\\": \\\"To ensure effective teaching, it is important to use clear and concise explanations, avoiding unnecessary jargon. Additionally, guiding students through the problem-solving process step by step and tailoring teaching strategies to cater to their individual needs are essential.\\\"}, {\\\"id\\\": 2, \\\"type\\\": [\\\"Guardrails\\\"], \\\"content\\\": \\\"Before processing students' questions, the tutor ensures that the answers come from lecture materials and removes students' personally identifiable information (PII) from the questions.\\\"}, {\\\"id\\\": 3, \\\"type\\\": [\\\"Instructions\\\"], \\\"content\\\": \\\"The tutor's approach includes carefully analyzing mathematical problems by reading and understanding the problem statement together with the student, identifying key information, and discussing and clarifying any unfamiliar terms or symbols. Additionally, the tutor determines the specific mathematical concepts and skills required to solve the problem.\\\"}, {\\\"id\\\": 4, \\\"type\\\": [\\\"Instructions\\\"], \\\"content\\\": \\\"In providing guidance, the tutor breaks down the problem into smaller, manageable steps, and guides the student through each step. Furthermore, the tutor demonstrates problem-solving strategies and provides clear explanations for each step, ensuring that the guidance provided is clear and understandable to students with poor math scores.\\\"}, {\\\"id\\\": 5, \\\"type\\\": [\\\"Audience\\\"], \\\"content\\\": \\\"The primary audience for this tutor is high school students who are good at statistic.\\\"}]}", "chain": null, "created_by": "sapper", "create_datetime": "2023-11-30T15:26:46", "update_datetime": "2023-11-30T15:26:57", "active": true}'''
        message = '''{"id": 1,"name": "test","image": "","spl": "{\\\"Persona\\\": {\\\"Description-0\\\": \\\"You are a marking system creator.\\\"}, \\\"Audience\\\": {\\\"Description-0\\\": \\\"Educators and instructors who need to assess student works.\\\"}, \\\"Terminology\\\": {\\\"Description-0\\\": \\\"Grading rubric\\\", \\\"Description-1\\\": \\\"Assessment criteria\\\", \\\"Description-2\\\": \\\"Weighted criteria\\\"}, \\\"ContextControl\\\": {\\\"Rule-0\\\": \\\"Design a flexible marking system that can accommodate various types of assignments and assessment criteria.\\\", \\\"Rule-1\\\": \\\"Ensure the marking system is user-friendly and intuitive for educators to use in assessing student works.\\\"}, \\\"Guardrails\\\": {\\\"PII\\\": \\\"Remove students' personally identifiable information from the marking system.\\\"}, \\\"Instruction-0\\\": {\\\"Name\\\": \\\"Create Marking System\\\", \\\"Commands\\\": [\\\"Determine the assessment criteria for the marking system.\\\", \\\"Design the grading rubric and scoring system based on the assessment criteria.\\\", \\\"Create a clear and concise documentation for the marking system.\\\", \\\"Test the marking system with sample student works to ensure accuracy and reliability.\\\"], \\\"Rules\\\": [\\\"Ensure the assessment criteria are relevant and aligned with the learning objectives.\\\", \\\"Use clear and understandable language in the grading rubric and documentation.\\\"]}}","spl_form": "{\\\"formData\\\": [{\\\"sectionId\\\": \\\"0\\\", \\\"sectionType\\\": \\\"Persona\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"You are a marking system creator.\\\"}]}, {\\\"sectionId\\\": \\\"1\\\", \\\"sectionType\\\": \\\"Audience\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Educators and instructors who need to assess student works.\\\"}]}, {\\\"sectionId\\\": \\\"2\\\", \\\"sectionType\\\": \\\"Terminology\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Grading rubric\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Description-1\\\", \\\"content\\\": \\\"Assessment criteria\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Description-2\\\", \\\"content\\\": \\\"Weighted criteria\\\"}]}, {\\\"sectionId\\\": \\\"3\\\", \\\"sectionType\\\": \\\"ContextControl\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Rule-0\\\", \\\"content\\\": \\\"Design a flexible marking system that can accommodate various types of assignments and assessment criteria.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Rule-1\\\", \\\"content\\\": \\\"Ensure the marking system is user-friendly and intuitive for educators to use in assessing student works.\\\"}]}, {\\\"sectionId\\\": \\\"4\\\", \\\"sectionType\\\": \\\"Guardrails\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"PII\\\", \\\"content\\\": \\\"Remove students' personally identifiable information from the marking system.\\\"}]}, {\\\"sectionId\\\": \\\"5\\\", \\\"sectionType\\\": \\\"Instruction-0\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Create Marking System\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Determine the assessment criteria for the marking system.\\\", \\\"Design the grading rubric and scoring system based on the assessment criteria.\\\", \\\"Create a clear and concise documentation for the marking system.\\\", \\\"Test the marking system with sample student works to ensure accuracy and reliability.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Ensure the assessment criteria are relevant and aligned with the learning objectives.\\\", \\\"Use clear and understandable language in the grading rubric and documentation.\\\"]}]}]}","nl": "{\\\"NL\\\": [{\\\"id\\\": 0, \\\"type\\\": [\\\"Persona\\\", \\\"Terminology\\\"], \\\"content\\\": \\\"The persona is an excellent high school mathematics tutor who specializes in areas such as algebra, geometry, and statistics.\\\"}, {\\\"id\\\": 1, \\\"type\\\": [\\\"ContextControl\\\"], \\\"content\\\": \\\"To ensure effective teaching, it is important to use clear and concise explanations, avoiding unnecessary jargon. Additionally, guiding students through the problem-solving process step by step and tailoring teaching strategies to cater to their individual needs are essential.\\\"}, {\\\"id\\\": 2, \\\"type\\\": [\\\"Guardrails\\\"], \\\"content\\\": \\\"Before processing students' questions, the tutor ensures that the answers come from lecture materials and removes students' personally identifiable information (PII) from the questions.\\\"}, {\\\"id\\\": 3, \\\"type\\\": [\\\"Instructions\\\"], \\\"content\\\": \\\"The tutor's approach includes carefully analyzing mathematical problems by reading and understanding the problem statement together with the student, identifying key information, and discussing and clarifying any unfamiliar terms or symbols. Additionally, the tutor determines the specific mathematical concepts and skills required to solve the problem.\\\"}, {\\\"id\\\": 4, \\\"type\\\": [\\\"Instructions\\\"], \\\"content\\\": \\\"In providing guidance, the tutor breaks down the problem into smaller, manageable steps, and guides the student through each step. Furthermore, the tutor demonstrates problem-solving strategies and provides clear explanations for each step, ensuring that the guidance provided is clear and understandable to students with poor math scores.\\\"}, {\\\"id\\\": 5, \\\"type\\\": [\\\"Audience\\\"], \\\"content\\\": \\\"The primary audience for this tutor is high school students who are good at statistic.\\\"}]}", "chain": null,"settings": null,"created_by": "sapper","create_datetime": "2023-12-02T04:42:38","update_datetime": "2023-12-02T04:42:38","active": true}'''
        await websocket.send(message)
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def formcopilot():
    # uri = "ws://localhost:8000/ws/sapperchain/formcopilot"
    uri = "wss://v1.promptsapper.tech/ws/sapperchain/formcopilot"
    async with websockets.connect(uri) as websocket:
        message = '''{"id": 1, "message": "I would like to add the primary school students as audience."}'''
        await websocket.send(message)
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def splcompiler():
    # uri = "ws://localhost:8000/ws/sapperchain/splcompiler"
    uri = "wss://v1.promptsapper.tech/ws/sapperchain/splcompiler"
    async with websockets.connect(uri) as websocket:
        message = '''{"id": 1, "name": "test", "image": "", "spl": "{\\\"Persona\\\": {\\\"Description-0\\\": \\\"An excellent high school mathematics tutor.\\\"}, \\\"Audience\\\": {\\\"Description-0\\\": \\\"High school students with poor math scores.\\\"}, \\\"Terminology\\\": {\\\"Description-0\\\": \\\"Algebra\\\", \\\"Description-1\\\": \\\"Geometry\\\", \\\"Description-2\\\": \\\"Statistics\\\"}, \\\"ContextControl\\\": {\\\"Rule-0\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\", \\\"Rule-1\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\", \\\"Rule-2\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}, \\\"Guardrails\\\": {\\\"Factuality\\\": \\\"The answers provided by the tutor must come from lecture materials.\\\", \\\"PII\\\": \\\"Remove students' PII from questions.\\\"}, \\\"Instruction-0\\\": {\\\"Name\\\": \\\"Analyze problem\\\", \\\"Commands\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"], \\\"Rules\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}, \\\"Instruction-1\\\": {\\\"Name\\\": \\\"Provide guidance\\\", \\\"Commands\\\": [\\\"Break down the problem into smaller, manageable steps, and guide the student through each step.\\\", \\\"Demonstrate problem-solving strategies and provide clear explanations for each step.\\\"], \\\"Rules\\\": [\\\"Avoid using advanced mathematical concepts that may overwhelm the student.\\\", \\\"Ensure that the guidance provided is clear and understandable to students with poor math scores.\\\"]}}", "spl_form": "{\\\"formData\\\": [{\\\"sectionId\\\": \\\"0\\\", \\\"sectionType\\\": \\\"Persona\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"An excellent high school mathematics tutor.\\\"}]}, {\\\"sectionId\\\": \\\"1\\\", \\\"sectionType\\\": \\\"Audience\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"High school students with poor math scores.\\\"}]}, {\\\"sectionId\\\": \\\"2\\\", \\\"sectionType\\\": \\\"Terminology\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Description-0\\\", \\\"content\\\": \\\"Algebra\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Description-1\\\", \\\"content\\\": \\\"Geometry\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Description-2\\\", \\\"content\\\": \\\"Statistics\\\"}]}, {\\\"sectionId\\\": \\\"3\\\", \\\"sectionType\\\": \\\"ContextControl\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Rule-0\\\", \\\"content\\\": \\\"Use clear and concise explanations, avoiding unnecessary jargon.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Rule-1\\\", \\\"content\\\": \\\"Guide students through the problem-solving process step by step, emphasizing the logic and reasoning behind each step.\\\"}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rule-2\\\", \\\"content\\\": \\\"Tailor your teaching strategies to cater to their individual needs and provide personalized assistance.\\\"}]}, {\\\"sectionId\\\": \\\"4\\\", \\\"sectionType\\\": \\\"Guardrails\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Factuality\\\", \\\"content\\\": \\\"The answers provided by the tutor must come from lecture materials.\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"PII\\\", \\\"content\\\": \\\"Remove students' PII from questions.\\\"}]}, {\\\"sectionId\\\": \\\"5\\\", \\\"sectionType\\\": \\\"Instruction-0\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Analyze problem\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Read and understand the problem statement together with the student.\\\", \\\"Identify the key information and any given conditions or constraints.\\\", \\\"Discuss and clarify any unfamiliar terms or symbols.\\\", \\\"Determine the specific mathematical concepts and skills required to solve the problem.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid overly complex or ambiguous phrasing.\\\", \\\"Provide appropriate explanations or mathematical concepts to facilitate user understanding.\\\"]}]}, {\\\"sectionId\\\": \\\"6\\\", \\\"sectionType\\\": \\\"Instruction-1\\\", \\\"sections\\\": [{\\\"subSectionId\\\": \\\"0\\\", \\\"subSectionType\\\": \\\"Name\\\", \\\"content\\\": \\\"Provide guidance\\\"}, {\\\"subSectionId\\\": \\\"1\\\", \\\"subSectionType\\\": \\\"Commands\\\", \\\"content\\\": [\\\"Break down the problem into smaller, manageable steps, and guide the student through each step.\\\", \\\"Demonstrate problem-solving strategies and provide clear explanations for each step.\\\"]}, {\\\"subSectionId\\\": \\\"2\\\", \\\"subSectionType\\\": \\\"Rules\\\", \\\"content\\\": [\\\"Avoid using advanced mathematical concepts that may overwhelm the student.\\\", \\\"Ensure that the guidance provided is clear and understandable to students with poor math scores.\\\"]}]}]}", "nl": "{\\\"NL\\\": [{\\\"id\\\": 0, \\\"type\\\": [\\\"Persona\\\", \\\"Terminology\\\"], \\\"content\\\": \\\"The persona is an excellent high school mathematics tutor who specializes in areas such as algebra, geometry, and statistics.\\\"}, {\\\"id\\\": 1, \\\"type\\\": [\\\"ContextControl\\\"], \\\"content\\\": \\\"To ensure effective teaching, it is important to use clear and concise explanations, avoiding unnecessary jargon. Additionally, guiding students through the problem-solving process step by step and tailoring teaching strategies to cater to their individual needs are essential.\\\"}, {\\\"id\\\": 2, \\\"type\\\": [\\\"Guardrails\\\"], \\\"content\\\": \\\"Before processing students' questions, the tutor ensures that the answers come from lecture materials and removes students' personally identifiable information (PII) from the questions.\\\"}, {\\\"id\\\": 3, \\\"type\\\": [\\\"Instructions\\\"], \\\"content\\\": \\\"The tutor's approach includes carefully analyzing mathematical problems by reading and understanding the problem statement together with the student, identifying key information, and discussing and clarifying any unfamiliar terms or symbols. Additionally, the tutor determines the specific mathematical concepts and skills required to solve the problem.\\\"}, {\\\"id\\\": 4, \\\"type\\\": [\\\"Instructions\\\"], \\\"content\\\": \\\"In providing guidance, the tutor breaks down the problem into smaller, manageable steps, and guides the student through each step. Furthermore, the tutor demonstrates problem-solving strategies and provides clear explanations for each step, ensuring that the guidance provided is clear and understandable to students with poor math scores.\\\"}, {\\\"id\\\": 5, \\\"type\\\": [\\\"Audience\\\"], \\\"content\\\": \\\"The primary audience for this tutor is high school students who are good at statistic.\\\"}]}", "chain": null, "created_by": "sapper", "create_datetime": "2023-11-30T15:26:46", "update_datetime": "2023-11-30T15:26:57", "active": true}'''
        await websocket.send(message)
        while True:
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()      

async def splemulator():
    # uri = "ws://localhost:8000/ws/sapperchain/splemulator"
    uri = "wss://v1.promptsapper.tech/ws/sapperchain/splemulator"
    async with websockets.connect(uri) as websocket:
        message = '''{"id": 1}'''
        await websocket.send(message)
        while True:
            message = input('input message >>> ')
            await websocket.send(message)
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def runchain():
    uri = "ws://localhost:8000/ws/sapperchain/runchain"
    # uri = "wss://v1.promptsapper.tech/ws/sapperchain/runchain"
    async with websockets.connect(uri) as websocket:
        message = '''{"id": 1}'''
        await websocket.send(message)
        while True:
            message = input('input message >>> ')
            await websocket.send(message)
            response = await websocket.recv()
            if response == "__END_OF_RESPONSE__":
                break
            else:
                print(f"{response}")
        await websocket.close()

async def upload_file():
    url = "http://localhost:8000/sapperchain/uploadfile"
    file_path = "knowledge.txt"
    try:
        async with httpx.AsyncClient() as client:
            async with aiofiles.open(file_path, 'rb') as file:
                content = await file.read()
                files = {'file': (file_path, content)}
                response = await client.post(url, files=files)
                print(response.json())  # or response.json() depending on the response
    except Exception as e:
        print(f"An error occurred: {e}")

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
            await nltosplform() 
        elif test_index == "4":
            await formcopilot() 
        elif test_index == "5":
            await splcompiler() 
        elif test_index == "6":
            await splemulator() 
        elif test_index == "7":
            await upload_file() 
        elif test_index == "8":
            await runchain() 
        else: 
            break


if __name__ == "__main__":
    asyncio.run(main())
