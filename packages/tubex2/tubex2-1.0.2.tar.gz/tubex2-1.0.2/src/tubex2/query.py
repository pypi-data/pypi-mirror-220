from tubex2 import Stream

class StreamQuery:
    def __init__(self, streams) -> None:
        self.streams: list[Stream] = streams

    def filter(self, _filters: dict):
        streams = []
        flag = True

        for stream in self.streams:
            for key, value in _filters.items():
                if key not in stream or stream[key] != value:
                    flag = False
                    break
            
            if flag:
                streams.append(stream)

            flag = True

        return StreamQuery(streams)
    
    def get_by_itag(self, itag: int) -> Stream | None:
        return self.filter({"itag": itag}).first()
    
    def all(self) -> list[Stream]:
        return self.streams
    
    def first(self):
        try:
            return self.streams[0]
        except:
            return None