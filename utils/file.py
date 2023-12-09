import requests
from io import BytesIO
import mimetypes
import asyncio


async def process_urls(urls):
    tasks = [get_file_from_bucket(url) for url in urls]
    files = await asyncio.gather(*tasks)
    attachments = []
    for i in files:
        attachments.append(("attachment", (f"file{i[1]}", i[0])))
    return attachments


async def get_file_from_bucket(url):
    chunk_size = 1024 * 4
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # read file in chunks
            file = BytesIO()
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
            file.seek(0)
            print(url)

            file_ext = mimetypes.guess_extension(url)

            return file, file_ext or ".dat"
        else:
            raise Exception("unable to get file from bucket")
    except Exception as e:
        raise e
