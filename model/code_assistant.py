import requests
import json
import os

class CodeAssistant:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.api_url = f"{self.base_url}/api/generate"
        self.headers = {'Content-Type': 'application/json'}
        self.history = []

    def generate_code(self, prompt):
        """Generates code using a local Ollama model (e.g., codellama)."""
        self.history.append(prompt)
        final_prompt = "\n".join(self.history)

        data = {
            "model": "codellama", # Ensure this model is pulled in Ollama
            "prompt": final_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
            if response.status_code == 200:
                response_text = response.text
                data = json.loads(response_text)
                actual_response = data['response']
                self.history.append(actual_response) # Add assistant response to history
                return actual_response
            else:
                return f"Error: {response.text}"
        except Exception as e:
            return f"Connection Error: {str(e)}. Is Ollama running?"

code_assistant = CodeAssistant()
