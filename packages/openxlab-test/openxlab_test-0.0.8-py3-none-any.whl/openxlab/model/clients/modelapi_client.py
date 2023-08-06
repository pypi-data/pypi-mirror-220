import requests

from openxlab.xlab.handler.user_token import get_jwt


class ModelApiClient(object):
    def __init__(self, endpoint, token):
        self.token = token
        self.endpoint = endpoint

    def get_inference_result(self, payload):
        """
        get inference result
        """
        result = self.http_post_response_dto(payload)
        return result

    def http_post_response_dto(self, payload):
        headers = self.http_common_header()
        response = requests.post(self.endpoint, files=payload["files"], data={'texts': payload['texts']}, headers=headers)
        response.raise_for_status()
        return response.content

    def http_common_header(self):
        try:
            jwt = get_jwt()
        except ValueError as e:
            print(f"warning: {e}")
            return
        header_dict = {
            "Authorization": jwt
        }
        return header_dict
