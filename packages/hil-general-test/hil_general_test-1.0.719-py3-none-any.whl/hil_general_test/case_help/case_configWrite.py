# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import socket
r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)

parser = argparse.ArgumentParser(description='mrtTest')
parser.add_argument('-i', type=bool, default = False,help="is distribution ")
parser.add_argument('-s', type=int, default = 0,help="start case index")
parser.add_argument('-e', type=int, default = None,help="end case index")
parser.add_argument('-m', type=str, default = None,help="env mapping path")
args = parser.parse_args()


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except:
        raise Exception("No Intranet IP was obtained!")
    finally:
        st.close()
    return IP


localIp = extract_ip()
case_config ={
        "is_distribution": args.i,
        "start_case": args.s,
        "end_case": args.e,
        "rtpc_host":localIp ,
        "mapping_path": args.m
}

case_config_json = json.dumps(case_config,indent=1)
_case_configPath = rootpath + "\\case_jsons\\case_run_config.json"
with open(_case_configPath, 'w',encoding='utf-8') as jsonf:
    jsonf.write(case_config_json)