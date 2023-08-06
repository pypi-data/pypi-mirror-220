import httpx
from tubex2 import Stream, StreamQuery, extract
from tubex2 import exceptions

import re
import json

class YouTube:
    def __init__(self, url) -> None:
        self._url = url
        self._js = None
        self._html = None
        self._streams = None
        self._basejs_url = None
        self._basejs_content = None
        self.video_id = extract.get_video_id(url)
    
    @property
    def basejs_url(self):
        if self._basejs_url is not None:
            return self._basejs_url 

        basejs_pattern = r'src="([^"]+base.js)"'

        result = re.search(basejs_pattern, self.html)
        
        self._basejs_url = "https://youtube.com" + result.group(1)

        return self._basejs_url
    
    @property
    def js(self):
        if self._js is not None:
            return self._js
        
        js_pattern = r"var ytInitialPlayerResponse = ([\s\S]*?)<\/script>"

        regex = re.compile(js_pattern)
        result = regex.search(self.html)

        self._js = json.loads(result.group(1)[:-1])

        return self._js
        
    @property
    def html(self):
        if self._html is not None:
            return self._html
        
        with httpx.Client() as client:
            self._html = client.get(self._url).text
        
        return self._html
    
    @property
    def streams(self) -> StreamQuery:
        if self._streams is not None:
            return StreamQuery(self._streams)
        
        if self.check_availability() is not None:
            raise exceptions.VideoUnavailable(video_id=self.video_id)
        
        self._streams = []
        
        for stream in extract.extend_stream(self.js["streamingData"]):
            if "s" in stream.keys():
                stream = extract.decode_signature(stream, self.basejs_content)

            video = Stream(stream, self.title)
            
            self._streams.append(video)

        return StreamQuery(self._streams)
    
    @property
    def title(self) -> str:
        if self.check_availability() is not None:
            raise exceptions.VideoUnavailable(video_id=self.video_id)

        return self.js["videoDetails"]["title"]
    
    @property
    def basejs_content(self):
        if self._basejs_content is not None:
            return self._basejs_content

        pattern = r"=function\(a\)(\{[^}]+\});"

        try:
            with httpx.Client() as client:
                js = client.get(self.basejs_url, follow_redirects=True).text
        except httpx.RequestError as e:
            raise exceptions.RequestError(f"HTTP request error: {e}")

        matching_functions = [match.group(1) for match in re.finditer(pattern, js) if 'a=a.split("")' in match.group(1)]
        
        if not matching_functions:
            raise exceptions.CustomFetchError("The desired function was not found in the JS content!")

        selected_function = matching_functions[0]

        pattern = r";(.*?)\."
        function_var_match = re.search(pattern, selected_function)

        if not function_var_match:
            raise exceptions.CustomFetchError("The function variable was not found in the JS content!")

        function_var = function_var_match.group(1)

        pattern = r'var %s\s*=\s*{[\s\S]*?};' % re.escape(function_var)
        function2_match = re.search(pattern, js)

        if not function2_match:
            raise exceptions.CustomFetchError("The second function was not found in the JS content!")

        selected_function2 = function2_match.group(0)
        
        self._basejs_content = f"{selected_function}\n{selected_function2}"

        return self._basejs_content

    def check_availability(self):
        status = self.js["playabilityStatus"]

        if status["status"] == "ERROR":
            return "ERROR"
        
        if "liveStreamability" in status:
            return "LIVE STREAM"
        
        return None