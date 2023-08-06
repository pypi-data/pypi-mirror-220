# tubex2

tubex2 is a Python library for download video from YouTube.

## Features
asynchronous video download

set the number of chunks

faster than other video download packages

get video url

many new features are under development

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install tubex2.

```bash
py -m pip install tubex2
```

## Usage

```python
from tubex2 import YouTube
import asyncio

async def get_video():
     url = "youtube-video-url"

     #create YouTube object
     yt = YouTube(url)

     #get stream
     stream = yt.streams.all().first()

     #download video
     await stream.download(num_chunks=10)

asyncio.run(get_video())
```
