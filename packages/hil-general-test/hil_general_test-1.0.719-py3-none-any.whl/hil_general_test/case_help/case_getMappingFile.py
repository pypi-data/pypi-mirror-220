import json
import os,sys

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from hil_general_test.case_help.case_configParser import Case_config


def download_caseFile(file_path, file_folder="/suite", isCover=True):
    from vcarhilclient.minio_handld import MinioClient
    minio_clint = MinioClient()
    if os.path.exists(file_path):
        if isCover:
            minio_clint.get_folderFile('buildsourse', f'/hil2.0{file_folder}', file_path)
    else:
        minio_clint.get_folderFile('buildsourse', f'/hil2.0{file_folder}', file_path)


def mapping_config_parser():
    mapping_path = rootpath + r"/case_env_mapping"
    download_caseFile(mapping_path,
                      f"/{Case_config.get_mapping_path()[3]}/{Case_config.get_mapping_path()[4]}")
    mapping_file = mapping_path + r"/rtpc_mapping_config.json"
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as jsonf:
            _mapping_config = json.load(jsonf)
    else:
        raise Exception(f"{mapping_file} not found!")
    for host , envs in _mapping_config.items():
        if host == Case_config.get_rtpcHost():
           return envs



# mapping_config_parser()
