#!/usr/bin/python
#
# - Foreword
# Simple script invoking ffmpeg and imagemagick convert tool to
# extract frames from a video file and mix them into a final
# image. The purpose is only artistic.
# 
# - Improvements
# Change external programs calls into a lib integration for
# both steps
#
# - Author
# heroncendre @github
#

import os, argparse, shutil, time, subprocess

def run_ffmpeg_cmd(args):
    basename = args.input.split('.')[0]
    dirname = "tmp-frames-%s" % basename
    os.makedirs(dirname)

    frame = "%s-%%03d.png" % basename
    cmd = "ffmpeg -i %s -ss %s -t %s -r %s %s/%s" % (args.input, args.start, args.duration, args.rate, dirname, frame)
    print "Run command: [%s]" % cmd
    subprocess.call(cmd, shell=True)
    return (dirname, frame)


def run_imagemagick_cmd(args, dirName, frame):
    # convert 1.jpg 2.jpg 3.jpg ... N.jpg -average result.jpg
    here = os.getcwd()
    os.chdir(dirName)
    nFrames = int(args.duration) * int(args.rate)
    cmdArgs = ""
    for i in range(nFrames):
        cmdArgs += frame % (i+1) 
        cmdArgs += " "
    output = "../average-%s.jpg" % time.strftime("%Y%m%d-%H%M%S")
    cmd = "convert %s -%s %s" % (cmdArgs, args.mix, output)
    print "Run command: [%s]" % cmd
    subprocess.call(cmd, shell=True)
    os.chdir(here)
    shutil.rmtree(dirName)


def main(args):
    print "Image mixer. Prerequisites: install ffmpeg and imagemagick tools."
    (dirname, frame) = run_ffmpeg_cmd(args)
    run_imagemagick_cmd(args, dirname, frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='image average stacking')
    parser.add_argument('-i', '--input',
        action='store',
        dest='input',
        help='input mp4 file'),
    parser.add_argument('-s', '--start',
        action='store',
        dest='start',
        help='start time'),
    parser.add_argument('-t', '--duration',
        action='store',
        dest='duration',
        help='duration'),
    parser.add_argument('-r', '--rate',
        action='store',
        dest='rate',
        help='extraction frame rate')
    parser.add_argument('-m', '--mix',
        action='store',
        dest='mix',
        default='average',
        help='mixing method')

    args = parser.parse_args()
    main(args)


