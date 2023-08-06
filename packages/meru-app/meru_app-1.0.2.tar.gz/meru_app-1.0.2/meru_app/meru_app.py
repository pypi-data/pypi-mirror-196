import requests
import json

class Meru:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def createIndex(self, file_url: str, index_name: str=None):
        if (not self.api_key):
            raise Exception("API Key not provided")

        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        url = "https://api.usemeru.com/refine/v4/files"
        data = {"files": file_url, **({"index_name": index_name} if index_name else {})}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

    def getIndex(self, file_id: str):
        if (not self.api_key):
            raise Exception("API Key not provided")

        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        url = f"https://api.usemeru.com/refine/v4/files/{file_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    def deleteIndex(self, file_id: str):
        if (not self.api_key):
            raise Exception("API Key not provided")

        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        url = f"https://api.usemeru.com/refine/v4/files/{file_id}"
        response = requests.delete(url, headers=headers)
        return response.json()

    def predict(self, file_id: str, prompt: str, temperature: float=None,
                    max_tokens: int=None, similarity_top_k: int=None):
        if (not self.api_key):
            raise Exception("API Key not provided")

        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        url = f"https://api.usemeru.com/refine/v4/predict"
        data = {
            "inputs": {
                "file_id": file_id,
                "prompt": prompt,
                **({"temperature": temperature} if temperature else {}),
                **({"max_tokens": max_tokens} if max_tokens else {}),
                **({"similarity_top_k": similarity_top_k} if similarity_top_k else {})
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

    def getPrediction(self, predict_id: str):
        if (not self.api_key):
            raise Exception("API Key not provided")

        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        url = f"https://api.usemeru.com/refine/v4/predict/{predict_id}"
        response = requests.get(url, headers=headers)
        return response.json()

    def deletePrediction(self, predict_id: str):
        if (not self.api_key):
            raise Exception("API Key not provided")

        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        url = f"https://api.usemeru.com/refine/v4/predict/{predict_id}"
        response = requests.delete(url, headers=headers)
        return response.json()