import requests

class Toxic(object):
    DOMAIN = "https://api-inference.huggingface.co"
    API_ENDPOINT = DOMAIN + "/models/unitary/unbiased-toxic-roberta"

    def __init__(self, query, token):
        super(Toxic, self).__init__()
        self.query = query
        self.response = ""
        self.token = token
        self.HEADERS = {"Authorization": "Bearer " + self.token}
        try:
            self.response = self.getScoreFromAPI()
        except Exception:
            self.response = "error in moderation layer"

    def check_toxicity(self, response_data):
        for label_info in response_data[0]:
            if label_info['score'] >= 0.8:
                return True
        return False

    def getScoreFromAPI(self):
        payload = {"inputs": self.query}
        response = requests.post(self.API_ENDPOINT, headers=self.HEADERS, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            self.check_toxicity(response_json)
            if self.check_toxicity(response_json):
                return "Sorry, we can't show this content as it is flagged as toxic."
            else:
                return self.query
        else:
            raise Exception("Hugging Face Space is down...")
