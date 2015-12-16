#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time
import subprocess, multiprocessing
from lib import audio_slice, config
from lib import process

SHOW_LOG            = True
CONFIG_FILENAME     = "../audio_process/config/config"


def run_cmds(cmds):
    for cmd in cmds:
        p               = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, err     = p.communicate()
        if SHOW_LOG:
            print("[ debug ]: ", output.decode('utf-8'))
            print("[ debug ]: Exit code:", p.returncode)


def get_all_media_files(input_dir, file_dic):
    if False == os.path.exists(input_dir):
        if SHOW_LOG:
            print("[ error ]: directory: %s is not exist. " % input_dir)
        return

    for root, dirs, files in os.walk(input_dir):
        for name in files:
            file                        = os.path.join(root, name)
            (short_name, extension)     = os.path.splitext(name)
            if (extension == ".mp4" or extension == ".flv" or extension == ".aac") and \
                    file not in file_dic.keys():
                file_dic[file]  = False
                if SHOW_LOG:
                    print("[ debug ]: found file : %s" % file)


def unhandled_files_filter( file_dic ):
    files = []
    for file, status in file_dic.items():
        if status == False:
            files.append(file)
    return files


def get_unhandled_files(input_dir, file_dic):
    get_all_media_files(input_dir, file_dic)
    return unhandled_files_filter(file_dic)



def run_audio_proc(filename):
    if SHOW_LOG:
        print("[ debug ]: Run child process to handle %s (%s)..." % (filename, os.getpid()))
    time.sleep(5)
    print("the end")
    cmds = audio_slice.get_ffmpeg_cmds(filename, ".")
    # run_cmds(cmds)


if __name__=='__main__':
    config_dic          = {}
    file_dic            = {}
    process_dic         = {}

    config.read_config(CONFIG_FILENAME, config_dic)
    input_filepath      = config_dic["path"]["scan_path"]
    output_m3u8path     = config_dic["path"]["output_m3u8_path"]
    slice_time          = config_dic["slice"]["hls_time"]
    max_process         = int(config_dic["process"]["max_process"])
    if SHOW_LOG:
        print("[ debug ]: Monitor directory is %s" % input_filepath)

    p = multiprocessing.current_process()
    p.daemon = True

    while True:
        cur_process = len(process_dic)

        if max_process > cur_process:
            files = get_unhandled_files(input_filepath, file_dic)
            if files:
                media_file = files.pop()
                process.create_process(process_dic, run_audio_proc, (media_file,))
                file_dic[media_file] = True

        process.destory_processes(process_dic)

        time.sleep(5)
