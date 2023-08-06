
import json
import os,sys

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)


_case_configPath = rootpath + r"/case_jsons/case_run_config.json"
with open(_case_configPath, 'r',encoding='utf-8') as jsonf:
    _case_json = json.load(jsonf)


class Case_config():

    @staticmethod
    def _get_is_distribution():
        is_distribution = _case_json["is_distribution"]
        return is_distribution

    @staticmethod
    def get_caseIndex():
        if Case_config._get_is_distribution():
            start_case = _case_json["start_case"]
            end_case = _case_json["end_case"]
            return int(start_case),int(end_case)+1
        else:
            return 0,None

    @staticmethod
    def get_rtpcHost():
        return _case_json["rtpc_host"]

    @staticmethod
    def get_mapping_path():
        mp = _case_json["mapping_path"]
        return mp.split("/")

    @staticmethod
    def get_job_name():
        return _case_json["job_name"]

    @staticmethod
    def get_job_number():
        return int(_case_json["job_number"])

    @staticmethod
    def get_case_file():
        return _case_json["case_file"]
