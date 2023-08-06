from urllib.parse import parse_qs
import re
from tubex2.exceptions import RegexMatchError

def mime_type_codec(mime_type):
    pattern = r"""(.+?);.*codecs=(".*?")"""

    regex = re.compile(pattern)
    result = regex.search(mime_type)

    return result.group(1), result.group(2)

def extend_stream(streams: dict) -> list[dict]:
    formats = []

    if "formats" in streams.keys():
        formats.extend(streams["formats"])
    if "adaptiveFormats" in streams.keys():
        formats.extend(streams["adaptiveFormats"])

    for stream in formats:
        if "url" not in stream:
            if "signatureCipher" in stream:
                cipher = parse_qs(stream["signatureCipher"])

                stream["url"] = cipher["url"][0]
                stream["s"] = cipher["s"][0]
    
    return formats

def get_video_id(url: str) -> str:
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=([a-zA-Z0-9_]+)|youtu\.be\/([a-zA-Z\d_]+))(?:&.*)?$"

    match = re.search(pattern, url)

    if match:
        video_id1 = match.group(1)
        video_id2 = match.group(2)

        if video_id1:
            return video_id1
        elif video_id2:
            return video_id2
    
    raise RegexMatchError(caller="get_video_id", pattern=pattern)

def decode_signature(stream, basejs_content: str):
    functions = basejs_content.split("\n")
    sig = list(stream["s"])
    
    functions[1] = functions[1][functions[1].index("{") + 1:-2]

    for op in functions[0][1:-1].split(";"):
        if "split" in op:
            continue
        
        index = function_index(functions[1:], op)

        if index == 0:
            _op = op[op.index("("):]
            b = int(re.search(r"\d+", _op).group())

            c = sig[0]
            sig[0] = sig[b % len(sig)]
            sig[b % len(sig)] = c
        
        elif index == 1:
            sig = sig[::-1]

        elif index == 2:
            _op = op[op.index("("):]

            b = int(re.search(r"\d+", _op).group(0))
            sig = sig[b:]

        else:
            sig = "".join(sig)

    stream["s"] = sig
    i = stream["url"].find("&lsparams")

    stream["url"] = stream["url"][:i] + "&sig=" + sig + stream["url"][i:]
    
    return stream

def function_index(function: list, var: str) -> int:
    for i, key in enumerate(function):
        if key[:key.index(":")] == var[var.index(".") + 1:var.index("(")]:
            if "splice" in key:
                return 2
            elif "reverse" in key:
                return 1
            else:
                return 0
    
    return 3