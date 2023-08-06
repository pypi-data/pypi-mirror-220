import argparse
import datetime
import ffmpeg
import os
import validators
import yt_dlp

parser = argparse.ArgumentParser()
parser.add_argument("video", help="url or path of the video you'd like to gif-ify")
parser.add_argument("start", type=lambda d: datetime.datetime.strptime(d, '%M:%S'), help="start time in minutes:seconds")
parser.add_argument("end", type=lambda d: datetime.datetime.strptime(d, '%M:%S'), help="end time in minutes:seconds")
parser.add_argument("--output", required=False, help="output file")
args = parser.parse_args()

start_sec = int(datetime.timedelta(minutes=args.start.minute, seconds=args.start.second).total_seconds())
end_sec = int(datetime.timedelta(minutes=args.end.minute, seconds=args.end.second).total_seconds())

if args.output:
    outputFile = args.output
else:
    outputFile = "result/output.gif"

if validators.url(args.video):
    URLS = [args.video]
    if os.path.exists("result/inter.mp4"):
        os.remove("result/inter.mp4")
    ydl_opts = {'final_ext': 'mkv',
                'download_ranges': yt_dlp.utils.download_range_func([], [[start_sec, end_sec]]),
                'format': 'bv*[ext=mp4]+ba[ext=vorbis]/b[ext=mp4] / bv*+ba/b',
                'outtmpl': {'default': 'result/inter.mp4'}}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)
    stream = ffmpeg.input('result/inter.mp4')
else:
    stream = ffmpeg.input(args.video)

stream = ffmpeg.filter(stream, 'scale', height=300, width=-2).output('result/inter-scale.mp4').run(overwrite_output=True)
stream = ffmpeg.input('result/inter-scale.mp4').filter('palettegen', stats_mode='full').output('result/palettegen_full.png')
stream = ffmpeg.run(stream, overwrite_output=True)
stream = ffmpeg.filter(
         [
            ffmpeg.input('result/inter-scale.mp4'),
            ffmpeg.input('result/palettegen_full.png'),

         ],
         filter_name='paletteuse',
         dither='heckbert',
         new='False',
         )
stream = ffmpeg.output(stream, outputFile, framerate=30)


def run() -> None:
    stream.run(overwrite_output=True)
    if os.path.exists("result/inter.mp4"):
        os.remove("result/inter.mp4")
    if os.path.exists("result/inter-scale.mp4"):
        os.remove("result/inter-scale.mp4")
    if os.path.exists("result/palettegen_full.png"):
        os.remove("result/palettegen_full.png")
