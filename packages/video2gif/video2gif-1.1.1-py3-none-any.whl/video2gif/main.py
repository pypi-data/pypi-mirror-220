import argparse
import datetime
import ffmpeg
import os
import validators
import yt_dlp
import uuid

parser = argparse.ArgumentParser()
parser.add_argument("video", help="url or path of the video you'd like to gif-ify")
parser.add_argument("start", type=lambda d: datetime.datetime.strptime(d, '%M:%S'), help="start time in minutes:seconds")
parser.add_argument("end", type=lambda d: datetime.datetime.strptime(d, '%M:%S'), help="end time in minutes:seconds")
parser.add_argument("--output", required=False, help="output file")
args = parser.parse_args()

start_sec = int(datetime.timedelta(minutes=args.start.minute, seconds=args.start.second).total_seconds())
end_sec = int(datetime.timedelta(minutes=args.end.minute, seconds=args.end.second).total_seconds())

projectRand = str(uuid.uuid4())
if args.output:
    outputFile = args.output
else:
    outputFile = f"{projectRand}.gif"


if validators.url(args.video):
    URLS = [args.video]
    if os.path.exists(f"result/{projectRand}.mp4"):
        os.remove(f"result/{projectRand}.mp4")
    ydl_opts = {'final_ext': 'mp4',
                'download_ranges': yt_dlp.utils.download_range_func([], [[start_sec, end_sec]]),
                'format': 'bv*[ext=mp4]+ba[ext=vorbis]/b[ext=mp4] / bv*+ba/b',
                'outtmpl': {'default': f'result/{projectRand}.mp4'}}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)
    stream = ffmpeg.input(f'result/{projectRand}.mp4')
else:
    stream = ffmpeg.input(args.video)

stream = ffmpeg.filter(stream, 'scale', height=300, width=-2).output(f'result/{projectRand}-scale.mp4').run(overwrite_output=True)
stream = ffmpeg.input(f'result/{projectRand}-scale.mp4').filter('palettegen', stats_mode='full').output(f'result/{projectRand}.png')
stream = ffmpeg.run(stream, overwrite_output=True)
stream = ffmpeg.filter(
         [
            ffmpeg.input(f'result/{projectRand}-scale.mp4'),
            ffmpeg.input(f'result/{projectRand}.png'),

         ],
         filter_name='paletteuse',
         dither='heckbert',
         new='False',
         )
stream = ffmpeg.output(stream, outputFile, framerate=30)


def run() -> None:
    stream.run(overwrite_output=True)
    if os.path.exists(f"result/{projectRand}.mp4"):
        os.remove(f"result/{projectRand}.mp4")
    if os.path.exists(f"result/{projectRand}-scale.mp4"):
        os.remove(f"result/{projectRand}-scale.mp4")
    if os.path.exists(f"result/{projectRand}.png"):
        os.remove(f"result/{projectRand}.png")
