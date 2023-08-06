
import os,sys

r=os.path.abspath(os.path.dirname(__file__))
rootpath= os.path.split(r)[0]
sys.path.append(rootpath)
import pytest
from hil_general_test.case_help.case_Logger import case_log
from hil_general_test.case_help.case_dataBase import HileDataBase
from hil_general_test.case_help.case_configParser import Case_config
from vcarhilclient.kunyi_mrt import mrt_client
from hil_general_test.case_help.case_pro_prepare import Pro_pre

@pytest.fixture(scope="session")
def manage_env():
    from hil_general_test.case_main.hil_general_test import hil_generalTest
    case_log.info(msg='\nThe test case data is ready...')
    pro = Pro_pre()
    bench = pro.get_testBench()
    ec = mrt_client(*bench).connet()
    if not (ec.value == 0):
        msg = f"Create test case fail ({ec.value}). Please check the status of your rtpc server at {bench}"
        case_log.error(msg)
        raise Exception(msg)
    else:
        case_log.info(msg=f"Successful connection to : {bench[0]}")

    # start test envs
    envNames = hil_generalTest.envNames
    for env in envNames:
        case_log.info(msg=f"start env: {env}")
        hil_generalTest.env_start(env)
    yield
    close_env()

def close_env():

    from hil_general_test.case_main.hil_general_test import mytest
    for env,test in mytest.items():
        rc = test.close()
        if rc == 0:
            case_log.info(msg=f"Destory env:{env} successful!")
        else:
            case_log.error(msg=f"Destory env:{env} failure! {rc}")

def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        case_name = item.name
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
        insertData = {"case_name": f"{case_name}", "sub_job_name": Case_config.get_job_name(),
                      "sub_job_number": Case_config.get_job_number(), "case_result": 1}
        db = HileDataBase()
        # re = db.select_db('cases', 'case_name', f"case_name = '{case_name}'")
        # if len(re) > 0:
        #     db.delete_db('cases', f"case_name = '{case_name}'")
        db.inset_db('cases', insertData)


def pytest_report_teststatus(report):

    if report.when in ("setup", "teardown"):
        if report.failed:
            case_name = report.head_line
            insertData = {"case_name": f"{case_name}", "sub_job_name": Case_config.get_job_name(),
                          "sub_job_number": Case_config.get_job_number(), "case_result":3}
            db = HileDataBase()
            re = db.select_db('cases', 'case_name', f"case_name = '{case_name}'")
            if len(re) == 0:
                db.inset_db('cases', insertData)
            else:
                db.update_db('cases', f'case_result=3',
                             f"case_name = '{case_name}' AND sub_job_number = {Case_config.get_job_number()}")
            return "error", "E", "ERROR"
        elif report.skipped:
            return "skipped", "s", "SKIPPED"
        else:
            return "", "", ""
    else:
        case_name = report.head_line
        case_status = report.outcome
        if case_status == 'passed':
            case_status = 4
        elif case_status == 'failed':
            case_status = 3
        else:
            case_status = -1

        insertData = {"case_name": f"{case_name}", "sub_job_name": Case_config.get_job_name(),
                      "sub_job_number": Case_config.get_job_number(), "case_result": case_status}
        db = HileDataBase()
        re = db.select_db('cases', 'case_name', f"case_name = '{case_name}'")
        if len(re) == 0:
            db.inset_db('cases', insertData)
        else:
            db.update_db('cases', f'case_result={case_status}',
                         f"case_name = '{case_name}' AND sub_job_number = {Case_config.get_job_number()}")
    return None






