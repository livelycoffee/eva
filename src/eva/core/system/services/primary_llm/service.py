from eva.core.system.services import Service
from eva.capabilities.executor import command_registry
from ollama import ChatResponse, chat
import os
import json
from pathlib import Path

file_path = Path(__file__)
src_path = file_path.parents[6]

class PrimaryLLMService(Service):
    def __init__(self):
        self.CHAT_LOG = src_path / f"storage/context/chat_log.json"
        self.context_history = None
        self.MODEL = "qwen3:4b-q4_K_M" # "qwen3:4b-q4_K_M" (recommended)

        self.SYSTEM_MESSAGE = """
            You are Eva, a very close friend and personal assistant to the user, who can help the user with tasks if asked. 
            Respond in short in only 1-2 sentences max, or maybe even less, until and unless specified by the user or absolutely necessary. 
            Never respond with emojis. 
            Use tools through tool-calling (with proper input) only when the user asks for a task to be done.

            Personality: Kawaii (teasingly cute), Friendly
        """ # --> TEMP
        self.TOOLS = command_registry
        self.MAX_HISTORY = 50

    def start(self):
        if not os.path.exists(self.CHAT_LOG):
            self.context_history = []
        else:
            try:
                with open(self.CHAT_LOG, "r") as file:
                    self.context_history = json.load(file)
            except Exception as e:
                print(f"[ERR - chat_log]: {e}")
                self.context_history = []
    
    def stop(self):
        with open(self.CHAT_LOG, "w") as file:
            json.dump(self.context_history, file, indent=2)

    def get_response(self, query: str, memories: str = "") -> str:
        tool_used = False
        tool_payload = []

        tool_handler = []
        if self.TOOLS is not None:
            tool_handler = list(self.TOOLS.values())
        
        response: ChatResponse = chat(model=self.MODEL, messages=[
            {
                'role': 'system',
                'content': self.SYSTEM_MESSAGE
            },
            *self.context_history[-5:],
            {
                'role': 'assistant',
                'content': f"Retrieved user memories: {memories}"
            },
            {
                'role': 'user',
                'content': query
            },
        ], tools=list(tool_handler), stream=False, think=False)

        if response.message.tool_calls:
            for tool in response.message.tool_calls or []:
                try:
                    func = self.TOOLS.get(tool.function.name)
                    if func:
                        print(f"[WARN]: {tool.function.name} TOOL WAS CALLED")
                        result = func(**tool.function.arguments)
                        tool_payload.append({
                            "tool": tool.function.name,
                            "args": tool.function.arguments,
                            "result": result
                        })
                        tool_used = True
                except Exception as e:
                    print(f"[ERR]: {e}")

        if tool_used:
            response: ChatResponse = chat(
                model=self.MODEL, # or MODEL_SMALL
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_MESSAGE # or SYSTEM_MESSAGE_SMALL
                    },
                    *self.context_history[-5:], # --> No history required if using MODEL_SMALL, do give for better results
                    {
                        "role": "assistant",
                        "tool_calls": response.message.tool_calls
                    },
                    {
                        "role": "tool",
                        "content": json.dumps(tool_payload)
                    }
                ], stream=False, think=False)

        self.context_history.append({"role": "user", "content": query})
        if tool_used:
            self.context_history.append({"role":"tool", "content": json.dumps(tool_payload)})
        self.context_history.append({"role":"assistant","content":str(response.message.content)})
        self.context_history = self.context_history[-self.MAX_HISTORY:]

        return str(response.message.content)
