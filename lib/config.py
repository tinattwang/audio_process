#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser, os

__all__ = [
    'read_config',
]

SHOW_LOG = True

def read_config(file, config_dic):
    if not os.path.exists(file):
        print("%s path not exist" % file)
        return

    conf        = configparser.ConfigParser()
    conf.read(file)
    sections    = conf.sections()

    for section in sections:
        temp_dict = {}
        if SHOW_LOG:
            print('[ debug ]: module name:[{}]'.format(section))
        for key in conf[section]:
            if SHOW_LOG:
                print("[ debug ]: read :[{}] = [{}]".format(key, conf[section][key]))
                temp_dict[key] = conf[section][key]
        config_dic[section] = temp_dict


if __name__ == '__main__':
    config_dic = {}
    read_config("../config/config", config_dic)
    for key in config_dic:
        if SHOW_LOG:
            print("[ debug ]: data dict:[{}] = [{}]".format(key, config_dic[key]))