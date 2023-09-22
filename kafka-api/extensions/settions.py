import os
import pathlib
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

default_path = __file__.split('\\')[-3]
mongo_db = 'kafka_9527'
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源进行跨域请求，您可以根据需求修改为特定的来源列表
    allow_credentials=True,  # 允许携带凭证（例如：cookies）
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


class ViewFile:
    path = './{}/views'.format(default_path)
    directory = pathlib.Path(
        __file__).parent.parent.parent.joinpath(path).as_posix()
    file_names = os.listdir(directory)
    modules = [file for file in file_names if '.' and '__' not in file]


class AppSettings:
    for mo in ViewFile.modules:
        path = f'./{default_path}/views/{mo}/api/'
        directory = pathlib.Path(
            __file__).parent.parent.parent.joinpath(path).as_posix()
        file_names = os.listdir(directory)
        modules = [file.rstrip('.py')
                   for file in file_names if not file.startswith('__')]
        for m in modules:
            imp = f"views.{mo}.api.{m}"
            router_module = importlib.import_module(imp)
            router = getattr(router_module, 'router')
            app.include_router(router)
