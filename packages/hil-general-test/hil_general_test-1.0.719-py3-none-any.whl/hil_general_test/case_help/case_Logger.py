import os
import sys
import time

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(os.path.split(r)[0])
import logging
from logging import handlers
from colorama import init
init(autoreset=True)

def handle_log(log_path,write_file=False):
    '''

    :param log_path；
    :return:
    '''
    log_file_name = time.strftime("%Y%m%d", time.localtime())
    log_dir = os.path.join(log_path,'{}_kyhil_generalTest.log'.format(log_file_name))
    kyAAT = logging.getLogger(name='kyHIL')

    pycharm = logging.StreamHandler()#Console channel
    #fomat
    # fmt = '\033[35m'+'%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(funcName)s-[line:%(lineno)d]：'+\
    #       '\033[0m\033[34m'+'%(message)s\033[0m'
    # filefmt = '%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(funcName)s-[line:%(lineno)d]：%(message)s'
    # fmt = '\033[35m'+'%(asctime)s-%(name)s-[%(levelname)s]:'+'\033[0m\033[34m'+'%(message)s\033[0m'
    fmt = '\033[35m'+'%(levelname)s    %(asctime)s: '+'\033[0m\033[34m'+'%(message)s\033[0m'
    filefmt = '%(levelname)s    %(asctime)s: %(message)s'


    kyAAT.setLevel(logging.DEBUG)
    log_fmt = logging.Formatter(fmt=fmt)
    log_fmt2 = logging.Formatter(fmt=filefmt)
    pycharm.setFormatter(fmt=log_fmt)

    #channel
    kyAAT.addHandler(pycharm)
    if write_file:
        file = handlers.TimedRotatingFileHandler(filename=log_dir, when='D', encoding='utf-8', interval=1,
                                                 backupCount=10)
        file.setFormatter(fmt=log_fmt2)
        kyAAT.addHandler(file)
    return kyAAT
case_log = handle_log(rootpath+'/case_log')

# case_log = logging.getLogger(__name__)

