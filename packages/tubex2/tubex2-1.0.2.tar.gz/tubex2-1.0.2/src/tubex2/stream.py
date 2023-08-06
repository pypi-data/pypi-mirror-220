from tubex2 import extract
import httpx
import asyncio

class Stream:
    def __init__(self, stream: dict, title: str) -> None:
        self.itag = int(stream["itag"])
        self.url = stream["url"]
        self.mime_type, self.codecs = extract.mime_type_codec(stream["mimeType"])
        self.bitrate = int(stream["bitrate"])
        self.quality = stream["quality"]
        self.type, self.extension = self.mime_type.split("/")
        if "fps" in stream:
            self.fps = int(stream["fps"])
            self.resolution = stream["qualityLabel"]

        if "s" in stream:
            self.sig = stream["s"]
        self._file_size = None
        self.title = title

    @property
    def file_size(self):
        if self._file_size is not None:
            return self._file_size
        
        with httpx.Client() as client:
            header = client.head(self.url)

        self._file_size = int(header.headers.get("Content-Length", 0))
        
        return self._file_size

    def __repr__(self) -> str:
        parts = [f""" itag: "{self.itag}" """, f""" mime_type: "{self.mime_type}" """, f""" codecs: "{self.codecs}" """, f""" bitrate: "{self.bitrate}" """]

        if "video" in self.mime_type:
            parts.append(
                f""" quality: "{self.resolution}" """
            )
        elif "audio" in self.mime_type:
            parts.append(
                f""" quality: "{self.quality}" """
            )

        return f"""<Stream: {" ".join(parts)}>"""
    
    async def __download_chunk(self, client, _from, _to, queue):
        headers = {"Range": f"bytes={_from}-{_to}"}

        async with client.stream("GET", self.url, headers=headers) as response:
            chunk = await response.aread()
            await queue.put((_from, chunk))

    async def download(self, filename=None, file_path="./", num_chunks=5):
        async with httpx.AsyncClient(http2=True) as client:
            chunk_size = self.file_size // num_chunks
            queue = asyncio.Queue()
            tasks = []

            for i in range(num_chunks):
                _from = i * chunk_size
                _to = _from + chunk_size - 1 if i < num_chunks - 1 else self.file_size - 1
                task = self.__download_chunk(client, _from, _to, queue)
                tasks.append(task)
            
            await asyncio.gather(*tasks)

            chunks = [b"" for _ in range(num_chunks)]

            while not queue.empty():
                _from, chunk = await queue.get()
                chunks[_from // chunk_size] = chunk

            if filename is None:
                filename = file_path + self.title + "." + self.extension

            with open(filename, "wb") as f:
                for chunk in chunks:
                    f.write(chunk)
        
        return filename
    
    def __contains__(self, key):
        return hasattr(self, key)

    def __getitem__(self, key):
        return getattr(self, key)