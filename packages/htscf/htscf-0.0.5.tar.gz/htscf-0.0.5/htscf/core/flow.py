import json
from subprocess import Popen, PIPE
from typing import Union
from functools import reduce
from htscf.db.mongo import connect
from uuid import uuid4
from pathlib import Path
from sys import platform


def workflow(rootPath: Union[Path, str], stepIds: list[str], dbName, stepsCollectionName, stepLogCollectionName, host, port):
    """
    流程化计算
    按照【stepIds】中的顺序在【rootPath】中运行【dbName】数据库【stepsCollectionName】中的每个step
    :param rootPath: 流程运行根目录
    :param stepsCollectionName: 具体存储流程的collection
    :param stepLogCollectionName: 每个流程记录的数据
    :param host: 数据库IP
    :param port: 数据库端口
    :param dbName: 数据库名
    :param stepIds: 按照顺序执行的过程ID
    """
    collection = connect(dbName, stepsCollectionName, host, port)
    stepLogCollection = connect(dbName, stepLogCollectionName, host, port)
    rootPath = Path(rootPath)
    rootPath.mkdir(exist_ok=True, parents=True)
    stepInfo = list(map(lambda i: dict(_id=i), stepIds))

    def runStep(prevStepInfo: Union[dict, str], currentStepInfo: dict) -> dict:
        prevData = None
        if prevStepInfo != "-1":
            prevData = stepLogCollection.find_one({
                "_id": prevStepInfo["logId"]
            })
        data = collection.find_one({
            "_id": currentStepInfo["_id"]
        })
        program = data["program"]
        scriptText = data["script"]
        settings = data["settings"]
        scriptFileName = f"script-{uuid4()}"
        settingsFileName = f"settings-{uuid4()}"
        (rootPath / scriptFileName).write_text(scriptText)
        (rootPath / settingsFileName).write_text(json.dumps(settings))
        args = [program, (rootPath / scriptFileName).absolute(), (rootPath / settingsFileName).absolute()]
        if prevData:
            prevDataFileName = f"prevData-{uuid4()}"
            (rootPath / prevDataFileName).write_text(json.dumps(prevData))
            args.append(prevDataFileName)
        popen = Popen(args, shell=True, stdout=PIPE)
        popen.wait()
        out = popen.stdout.read()
        print(out)
        try:
            if platform == "win32":
                outData = out.decode("gbk")
            else:
                outData = out.decode("utf-8")
        except Exception as e:
            print(e)
            outData = out.decode("utf-8")
        logId = f"{currentStepInfo['_id']}-{uuid4()}"
        stepLogCollection.insert_one({
            "_id": logId,
            "data": outData
        })
        return {
            "_id": currentStepInfo["_id"],
            "logId": logId
        }

    reduce(runStep, stepInfo, "-1")
