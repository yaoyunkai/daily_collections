"""

UploadFile:
    filename
    content_type
    file: file object

async 方法
    write
    read
    seek
    close

    contents = await myfile.read()

contents = myfile.file.read()



Created at 2023/7/10
"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    """
    如果把路径操作函数参数的类型声明为 bytes，FastAPI 将以 bytes 形式读取和接收文件内容。

    """
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


def get_module_name() -> str:
    file_name = os.path.basename(__file__)
    file_name = file_name.replace('.py', '')

    return file_name


if __name__ == '__main__':
    uvicorn.run(f'{get_module_name()}:app', reload=True, port=9000)
