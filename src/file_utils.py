import aiofiles


async def read_text_file_async(file_path):
    content: str = ""
    async with aiofiles.open(file_path, mode="tr") as file:
        content = await file.read()
    return content
