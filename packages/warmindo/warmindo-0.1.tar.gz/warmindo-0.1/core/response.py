class Response:
    def __init__(self, content, status_code=200, content_type='text/html'):
        self.content = content
        self.status_code = status_code
        self.content_type = content_type

    def render(self):
        return self.content