class CustomFetchError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

class RequestError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

class RegexMatchError(Exception):
    def __init__(self, caller, pattern) -> None:
        super().__init__(f"{caller}: couldn't find match for {pattern}")
        self.caller = caller
        self.pattern = pattern

class VideoUnavailable(Exception):
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        super().__init__(self.error_string)
    
    @property
    def error_string(self):
        return f"{self.video_id} is unavailable"