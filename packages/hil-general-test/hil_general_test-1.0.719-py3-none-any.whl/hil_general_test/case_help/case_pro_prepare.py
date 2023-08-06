import json
import os, sys

r = os.path.abspath(os.path.dirname(__file__))
rootpath = os.path.split(r)[0]
sys.path.append(rootpath)

from vcarhilclient.minio_handld import MinioClient
from hil_general_test.case_help.case_jsonParser import Case_json
from hil_general_test.case_help.case_Logger import case_log
from hil_general_test.case_help.case_configParser import Case_config
from hil_general_test.case_help.case_getMappingFile import mapping_config_parser


class Pro_pre():

    def __init__(self):
        self.em_pro = Case_json.get_EM_project()
        self.suite = Case_json.get_suit()
        self.envNemes = Case_json.get_env_names()
        self.em_pro_Path = os.path.dirname(r) + f'/ip_projects/{self.em_pro}'
        self.download_proFile()
        self.emrPath = self.get_emrFile(self.em_pro_Path)
        with open(self.emrPath, encoding='utf-8') as f:
            self.emrFile = json.load(f)

    def get_proInfo(self):

        envInfos = []
        pro_env = []
        envCount = 0
        for i in self.emrFile["EnvironmentList"]:
            envInfo = []
            ProjectFilePath = i["ProjectFilePath"]
            MappingFilePath = i["MappingFilePath"]
            ProjectFilePath = ProjectFilePath.replace("\\", "/")
            MappingFilePath = MappingFilePath.replace("\\", "/")
            EnvironmentName = i["EnvironmentName"]
            pro_env.append(EnvironmentName)
            if EnvironmentName in self.envNemes:
                envInfo.append(EnvironmentName)
                envInfo.append(os.path.join(self.em_pro_Path, ProjectFilePath))
                if EnvironmentName in mapping_config_parser():
                    MappingFilePath = os.path.join(rootpath + r"/case_env_mapping",
                                                   mapping_config_parser()[EnvironmentName])
                envInfo.append(os.path.join(self.em_pro_Path, MappingFilePath))
                envInfos.append(envInfo)
            else:
                info = f"EnvironmentNames pro env:'{EnvironmentName}' not in c" \
                       f"ase suite:{self.suite},so no testing required "
                case_log.info(msg=info)
        for env in self.envNemes:
            if env not in pro_env:
                msg = f"'{env}'not found in this project [{self.em_pro}>>{tuple(pro_env)}]," \
                      f"Please check the case suite:{self.suite} parameters'env_names'"
                case_log.error(msg=msg)
                raise Exception(msg)
            else:
                envCount += 1
        if envCount == 0:
            ex = f" case suite:{self.suite} parameters 'env_names' envs all not found in this " \
                 f"project [{self.em_pro}>>{pro_env}] ,\nPlease check the case suite:{self.suite} parameters'env_names'"
            case_log.error(msg=ex)
            raise Exception(ex)

        return envInfos

    def get_testBench(self):
        testBench = []
        testBench_dict = self.emrFile["TestBenchLocation"]
        testBench_dict["IP"] = Case_config.get_rtpcHost()
        # testBench_dict["ControlPort"] = '8877'
        for k, v in testBench_dict.items():
            testBench.append(str(v))
        return testBench

    def download_proFile(self, isCover=True):
        minio_clint = MinioClient()

        pro_savePath = self.em_pro_Path + '.zip'
        if os.path.exists(pro_savePath):
            if isCover:
                minio_clint.download_file('buildsourse', f'emr/{self.em_pro}.zip', pro_savePath)
        else:
            minio_clint.download_file('buildsourse', f'emr/{self.em_pro}.zip', pro_savePath)
        if os.path.exists(self.em_pro_Path):
            if isCover:
                self.pro_uncompress(pro_savePath, os.path.dirname(r) + '/ip_projects/')
        else:
            self.pro_uncompress(pro_savePath, os.path.dirname(r) + '/ip_projects/')

    def pro_uncompress(self, filPath, targetPath):
        import shutil
        shutil.unpack_archive(filPath, targetPath)
        return targetPath

    def get_emrFile(self, file_rootdir):
        fileList = os.listdir(file_rootdir)
        emrFile = None
        for file in fileList:
            if file.split(".")[-1] == "emr":
                emrFile = os.path.join(file_rootdir, file)
        if emrFile is None:
            ex = "Emr File(*.emr) is not correct or Emr File(*.emr) is missing "
            case_log.error(msg=ex)
            raise Exception(ex)
        return emrFile
