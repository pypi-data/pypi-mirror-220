import requests as r

class Maglev:
    def __init__(self, api_key):
        self.api_base_url = "https://api.maglevai.com"
        self.api_key = api_key

    def hallucinations(self, prompt, content):
        endpoint = "/hallucinations/"
        url = f"{self.api_base_url}{endpoint}"
        headers = {
                    f"Authorization": "Bearer {self.api_key}"
                }

        data = {
            "prompt": prompt,
            "content": content,
        }

        response = r.post(url, json=data, headers=headers)

        if str(response.status_code) == '200':
            response_json = response.json()
            if "NO" in response_json['is_passed_hallucination_check'].upper():
                return False
            else:
                return True
        else:
            return "Error Code: " + str(response.status_code)

