
import os ,sys
import time

r=os.path.abspath(os.path.dirname(__file__))
rootpath= os.path.split(r)[0]
sys.path.append(rootpath)

from vcarhilclient.kunyi_project import *
from hil_general_test.case_help.case_pro_prepare import Pro_pre
from hil_general_test.case_help.case_jsonParser import Case_json
from hil_general_test.case_help.case_Logger import case_log
from vcarhilclient.kunyi_hil_test import hil_test
from vcarhilclient.kunyi_mrt import mrt_client


class Case_dataPrepare():

    def __init__(self):

        pro = Pro_pre()
        self.pro_info = pro.get_proInfo()
        self.bench = pro.get_testBench()
        self.cases = Case_json.get_cases()
        self.test_suite_name = Case_json.get_test_suite_name()
        self.envNames = []
        self.mytests = {}
        self.benchInfo = ''

    def env_init(self):

        try:
            rtpc_client = mrt_client(*self.bench)
            case_log.info(f"Connection to : {self.bench}")
        except:
            ex = "Connection information error"
            case_log.error(msg=ex)
            raise Exception(ex)
        en = ''
        for env_name , ip_project_path, mapping_path in self.pro_info:
            en = env_name
            self.envNames.append(env_name)
            mytest = hil_test(ip_project_path, rtpc_client, env_name, mapping_path, os.path.dirname(ip_project_path))
            self.mytests[env_name] = mytest
        mrt_v = self.mytests[en].get_mrtClientVersion()
        rtpc_v = self.mytests[en].get_rtpcVersion()
        if mrt_v == rtpc_v:
            self.benchInfo = f"\n\t *** mrtClientVersion:{mrt_v} ,rtpcVersion:{rtpc_v} ***"
            case_log.info(msg=self.benchInfo)
        else:
            self.benchInfo = f"\n\t*** mrtClientVersion:{mrt_v} and rtpcVersion:{rtpc_v} are not equal!it may cause unforeseen errors! ***"
            case_log.warning(msg=self.benchInfo)

    def env_start(self,envName):
        self.mytests[envName].prepare_test_env()

    def check_sequence(self):

        cases = self.cases
        sequence = []
        for case in cases:
            sequence.append(case["execute_sequence"])
        sequence.sort()
        sequence = list(set(sequence))
        return sequence

    def check_caseIndex(self,full_cases,start_case,end_case):
        if start_case:
            if start_case > len(full_cases):
                msg = f"\n\tThere are no case to test(All cases: {len(full_cases)}," \
                      f"\n\tChoose case {start_case} ~ {end_case}!) \n\tSo quit this test!"
                case_log.warning(msg=msg)
                raise Exception(msg)
            if end_case:
                if start_case > end_case:
                    msg = f"\n\t case index config Error!start_case:{start_case} can not >(greater than) end_case:{end_case} "
                    case_log.warning(msg=msg)
                    raise Exception(msg)


    def case_analyse(self):

        self.env_init()
        sequence = self.check_sequence()
        cases = self.cases
        final_cases = []
        # caseNames = ["run test fot case name","test0_cal_Scalar测试","test0_cal_Map"]
        for s in sequence:
            for case in cases:
                # run test fot case name
                # if case["case_name"] not in caseNames:
                #     continue
                # Reorganize test case priorities
                if case["execute_sequence"] == s:
                    caseInfo = {}
                    steps = []
                    id = 0
                    for step in case["steps"]:
                        # stepId = f"{case['case_name']}_{id}"
                        stepId = id
                        k = step["keyword"].lower()
                        if k in ["write", "read", "wait"]:
                            case_step = {}
                            if k == "wait":
                                value = step["value"]
                                case_step[stepId] = (k, value)
                            elif k != "wait":
                                test_envName = step["var_env_name"]
                                portType = step["var_type"].lower()
                                instance = step["var_instance"]
                                signalName = step["var_signal_name"]
                                expect = step["expect"]
                                if test_envName not in self.envNames:
                                    msg = f"\n\tCASE: '{case['case_name']} \n\tSTEP{stepId}:\n\tenv:'{test_envName}' " \
                                          f"is not running or not exist in the project{tuple(self.envNames)}"
                                    case_log.error(msg=msg)
                                    # case_step[stepId] = ("error", 0)
                                    # steps.append(case_step)
                                    # id += 1
                                    raise Exception(msg)
                                    # continue
                                if k == "write":
                                    if portType == "calibrations":
                                        cal_type = step["var_cal_type"]
                                        cal_xlength = step["var_cal_xlength"]
                                        cal_ylength = step["var_cal_ylength"]
                                        cal_funlength = step["var_funlength"]
                                        cal_xidx = step["var_cal_xidx"]
                                        cal_yidx = step["var_cal_yidx"]
                                        cal_funidx = step["var_cal_funidx"]
                                        cal_value_array = step["var_cal_value_array"]
                                        sn,portTypeId,cal_dt = self.mytests[test_envName].get_calInfo(instance, portType,
                                                                                                      cal_type,signalName)
                                        case_step[stepId] = (k, test_envName, instance, signalName,cal_dt,None,
                                                             portTypeId,expect,cal_xlength,cal_ylength,
                                                             cal_funlength,cal_xidx,cal_yidx,cal_funidx,cal_value_array )
                                    else:
                                        value = step["value"]
                                        struct_detail = step["var_struct_detail"]
                                        dataType, itemCount, portTypeId = self.mytests[test_envName].get_signalInfo(instance,
                                                                                                                    portType,
                                                                                                                    signalName)
                                        case_step[stepId] = (k, test_envName, instance, signalName,
                                                             dataType, value, portTypeId, itemCount,
                                        struct_detail, expect)
                                elif k == "read":
                                    if portType == "calibrations":
                                        cal_type = step["var_cal_type"]
                                        cal_xlength = step["var_cal_xlength"]
                                        cal_ylength = step["var_cal_ylength"]
                                        cal_funlength = step["var_funlength"]
                                        cal_xidx = step["var_cal_xidx"]
                                        cal_yidx = step["var_cal_yidx"]
                                        cal_funidx = step["var_cal_funidx"]
                                        sn,portTypeId,cal_dt = self.mytests[test_envName].get_calInfo(instance,
                                                                                                      portType, cal_type,signalName)
                                        case_step[stepId] = (k, test_envName, instance, signalName,cal_dt,portTypeId,
                                                             expect,cal_xlength,cal_ylength,
                                                             cal_funlength,cal_xidx,cal_yidx,cal_funidx)

                                    else:
                                        struct_detail = step["var_struct_detail"]
                                        dataType, itemCount, portTypeId = self.mytests[test_envName].get_signalInfo(instance,
                                                                                                                    portType,
                                                                                                                    signalName)
                                        case_step[stepId] = (
                                        k, test_envName, instance, signalName, dataType, portTypeId, itemCount,
                                        struct_detail, expect)
                            steps.append(case_step)
                            id += 1
                        else:
                            erro = f"\n\tPlease check the json parameters'keyword',[{k}] not support!"
                            case_log.error(msg=erro)
                            raise Exception(erro)
                    caseInfo[case['case_name']] = steps
                    final_cases.append(caseInfo)
        return final_cases
    '''
            :return data layout
        [
            {
                "case1": [
                    {
                        "case1_step_1": [
                            "write",#keyward
                            "env_1",
                            "expression_1",
                            "x[1]",
                            "Double", 
                            56, #signal value
                            0, #portType ID
                            1, #itemCount
                            null, #struct_detail
                            {   
                                ### expect
                                "left_target": "rc[1][0].port_type",
                                "right_target": "t_v[]",
                                "operator": "==",
                                "expect_data_type": "",
                                "expect_value": ""
                            }
                        ]
                    },
                    {
                        "case1_step_2": [ ...
                        ]
                    },
                    {
                        "case1_step_3": [
                            "wait",
                            2
                        ]
                    }
                ]
            },
            {
            ...
            }
        ]
            '''


class Case_Step():

    def __init__(self,mytest):
        self.mytest = mytest

    def key_word_write(self,test_envName,*args):
        re = self.mytest[test_envName].writePort(*args)
        return re

    def write_cal(self,test_envName,*args):
        re = self.mytest[test_envName].write_cal(*args)
        return re

    def key_word_read(self,test_envName,*args):
        re = self.mytest[test_envName].readPort(*args)
        return re

    def read_cal(self,test_envName,*args):
        re = self.mytest[test_envName].read_cal( *args)
        return re

    def key_word_wait(self,t):
        print(f"\n\tcase sleep {t}")
        time.sleep(t)

    def expect_parse(self,expect,cn,stepid,result,expect_id):
        ex_v = []
        lf_ex_v = []
        expectValue = False
        Left_right_assertion = False
        ex_msg = ''
        lf_ex_msg =''
        expect_data_type = expect["expect_data_type"]

        expect_value = expect["expect_value"]
        if expect_value:
            if self.try_typeChange(result[stepid]) == self.try_typeChange(expect_value):
                ex_msg = f"\n\t>>  RESULT: {str(result[stepid])} \n\t>>  OPERATOR: = \n\t>>  EXPECT: {str(expect_value)}"
                expectValue = True
            else:
                ex_msg = f"\n\t>>  RESULT: {str(result[stepid])} \n\t>>  OPERATOR: != \n\t>>  EXPECT: {str(expect_value)}"
        else:
            expectValue = "no use"
            case_log.warning(msg=f"\n\t>>  CASE NAME: {cn}\n\tCASE STEP{stepid}\n\tCASE EXPECT ID: "
                                 f"expect {expect_id}>>  'ExpectValue_assertion' can not use;")

        left_target = expect["left_target"]
        right_target = expect["right_target"]
        leftTraget = ''
        rightTarget = ''
        if left_target:
            if type(left_target) is str :
                if left_target.lower().split("[")[0] == "result":
                    s ='left='
                    exec(s+left_target)
                    leftTraget = locals()['left']

                else:
                    leftTraget = left_target

            else:
                leftTraget = left_target

        if right_target:
            if type(right_target) is str:
                if right_target.lower().split("[")[0]== "result":
                    s ='right = '
                    exec(s + right_target)
                    rightTarget = locals()['right']
                else:
                    rightTarget = right_target
            else:
                rightTarget = right_target

        leftTraget = self.try_typeChange(leftTraget)
        rightTarget = self.try_typeChange(rightTarget)
        ope = expect["operator"]
        if ope and left_target and right_target:
            Left_right_assertion = self.operator_check(ope.lower(),leftTraget,rightTarget)
            if not Left_right_assertion:
                lf_ex_msg = f"\n\t>>  LEFT_TARGET: {leftTraget} \n\t>>  OPERATOR: !{ope} \n\t>>  RIGHT_TARGET: {rightTarget} "
            else:
                lf_ex_msg = f"\n\t>>  LEFT_TARGET: {leftTraget} \n\t>>  OPERATOR: {ope} \n\t>>  RIGHT_TARGET: {rightTarget} "
        else:
            Left_right_assertion = "no use"
            case_log.warning(msg=f"\n\t>>  CASE NAME: {cn}\n\tCASE STEP{stepid}\n\tCASE EXPECT "
                                 f"ID: expect {expect_id}>>  'Left_right_assertion' can not use;")
        ex_v.append(expectValue)
        ex_v.append(ex_msg)
        lf_ex_v.append(Left_right_assertion)
        lf_ex_v.append(lf_ex_msg)
        return ex_v , lf_ex_v

    def try_typeChange(self,arg):
        try:
            tc = float(arg)
            return tc
        except:
            try:
                tc = list(arg)
                return tc
            except:
                return arg

    def operator_check(self,ope,left_target,right_target):
        if ope in ["==", ">=", "<=", ">", "<", "in", "not in","notin"]:
            if ope == "==":
                if left_target == right_target:
                    return True
            if ope == ">=":
                if left_target >= right_target:
                    return True
            if ope == ">=":
                if left_target >= right_target:
                    return True
            if ope == "<=":
                if left_target <= right_target:
                    return True
            if ope == ">":
                if left_target > right_target:
                    return True
            if ope == "<":
                if left_target < right_target:
                    return True
            if ope == "in":
                if left_target in right_target:
                    return True
            if ope == "not in" or ope == "notin":
                if left_target not in right_target:
                    return True
        else:
            case_log.warning(msg=f"operator:'{ope}' ,does not support! support>>  ['==', '>=', '<=', '>', '<', 'in','not in']")

    def assertion_log(self,expectValue,Left_right_assertion,cn,stepid,expectid,kword,stepData):

        if not expectValue[0]:
            case_log.error(msg=f"\n\tExpectValue_assertion: Assertion Error! "
                               f"\n\t>>  CASE NAME: {cn}\n\t>>  CASE KEY WORD: {kword}"
                               f"\n\t>>  CASE STEP: step {stepid}\n\t>>  STEP DATA:\n\t{stepData}"
                               f"\n\t>>  CASE EXPECT ID: expect {expectid}{expectValue[1]}")
        elif expectValue[0] == True:
            case_log.info(msg=f"\n\tExpectValue_assertion: Assertion Successful! "
                              f"\n\t>>  CASE NAME: {cn}\n\t>>  CASE KEY WORD: {kword}"
                              f"\n\t>>  CASE STEP: step {stepid}\n\t>>  STEP DATA:\n\t{stepData}"
                              f"\n\t>>  CASE EXPECT ID: expect {expectid}{expectValue[1]}")

        if not Left_right_assertion[0]:
            case_log.error(msg=f"\n\tLeft_right_assertion: Assertion Error! \n\t>>  CASE NAME: {cn}"
                               f"\n\t>>  CASE KEY WORD: {kword}\n\t>>  CASE STEP: step {stepid}"
                               f"\n\t>>  STEP DATA:\n\t{stepData}\n\t>>  CASE EXPECT ID: expect {expectid}{Left_right_assertion[1]}")
        elif Left_right_assertion[0] == True:
            case_log.info(msg=f"\n\tLeft_right_assertion: Assertion Successful! "
                              f"\n\t>>  CASE NAME: {cn}\n\t>>  CASE KEY WORD: {kword}"
                              f"\n\t>>  CASE STEP: step {stepid}\n\t>>  STEP DATA:\n\t{stepData}"
                              f"\n\t>>  CASE EXPECT ID: expect {expectid}{Left_right_assertion[1]}")
