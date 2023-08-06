# Copyright 2023 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.


class InMemoryTokenProvider:

    def __init__(self, token: str):
        self._token = token

    def get_access_token(self):
        return self._token
