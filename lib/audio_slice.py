#! /usr/bin/env python3
import os

__all__ = [
    'get_ffmpeg_cmds',
]

SHOW_LOG = True

def get_ffmpeg_cmds(input_file, output_dir=".", hls_list_size="0", hls_time="10"):
    if len(input_file) <= 0:
        return

    cmds                    = []
    (dirname, filename)     = os.path.split(input_file)
    (shortname, extension)  = os.path.splitext(filename)
    src_file             = input_file

    if extension == ".mp4":
        aacfile = os.path.join(output_dir, shortname + ".aac")
        cmd = "ffmpeg -i {input} -acodec copy -vn {output}".format(input=input_file, output=aacfile)
        cmds.append(cmd)
        src_file = aacfile

    if extension == ".flv":
        pass

    if extension == ".mp3":
        pass

    output_m3u8file = os.path.join(output_dir, shortname + ".m3u8")
    cmd = "ffmpeg -i {input} -c:a aac -strict -2 -f hls -hls_list_size {size} -hls_time {time} {output}" \
        .format(input=src_file, size=hls_list_size, time=hls_time, output=output_m3u8file)
    cmds.append(cmd)

    return cmds


if __name__ == '__main__':
    src_file    = "/media/SeeYouAgain-Trench.mp4"
    output_dir  = "/usr/local/nginx/html/media"
    cmds        = get_ffmpeg_cmds(src_file, output_dir)

    for cmd in cmds:
        if SHOW_LOG:
            print("[ debug ]: ", cmd)