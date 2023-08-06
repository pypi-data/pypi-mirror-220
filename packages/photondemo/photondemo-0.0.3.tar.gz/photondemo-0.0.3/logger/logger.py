import requests


class PhotonLogger:
    def __init__(self, *args, **kwargs) -> None:
        self.photon_url = "http://beacon-demo-production.up.railway.app/api"

    def log_output(self, payload):
        response = requests.post(self.photon_url, json=payload)
        return response