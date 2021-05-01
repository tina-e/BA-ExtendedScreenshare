# ffmpeg

# command line:
# ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 output.mp4
#                    breite x hoehe                             startpunkt

# https://pypi.org/project/python-ffmpeg-video-streaming/


# import ffmpeg_streaming
# capture = ffmpeg_streaming.input(':0.0+100,200', capture=True)

# ffmpeg -f x11grab -r 1 -loglevel panic -s `xdpyinfo | grep 'dimensions:'|awk '{print $2}'` -i $DISPLAY -qscale 0 -f mpegts udp://localhost



# WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS - WORKS
# http://morrillplou.me/blog/index.php/2019/03/04/streaming-video-over-lan-with-ffmpeg/
# !!! use IP of accessing device not streming device !!!
# streaming: ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 -preset ultrafast -tune zerolatency -codec libx264 -f mpegts udp://192.168.178.169:8000/
# streaming: ffmpeg -video_size 1024x768 -framerate 25 -f x11grab mpegts udp://192.168.178.169:8000/ -i :0.0+100,200
# accessing: ffplay -f mpegts udp://192.168.178.136:8000
import subprocess

x_pos = 100
y_pos = 100
width = 750
height = 500
ip_receiver = '192.168.178.136'
port = 9000

def start_stream():
    subprocess.Popen(f"ffmpeg -video_size {width}x{height} -framerate 25 -f x11grab -i :0.0+{x_pos},{y_pos} -f mpegts udp://{ip_receiver}:{port}", shell=True)

def access_stream():
    subprocess.check_output(f"ffplay -f mpegts udp://{ip_receiver}:{port}/", shell=True)


start_stream()
access_stream()
# !!! end streams manually / dont re-run, stop !!!


#import ffmpeg

#options = {'video_size': '1024x768', 'framerate': 25, 'f': 'x11grab', 'f': 'mpegts udp://192.168.178.136:8000/'}
#stream = ffmpeg.input(':0.0+100,200', video_size='1024x768', framerate=25, format_options='x11grab | mpegts udp://192.168.178.136:8000/')

#print(stream)
#ffmpeg.run(stream)


import ffmpeg_streaming
#capture = ffmpeg_streaming.input(':0.0+100,200', video_size='1024x768', framerate=25, format='x11grab', fmpegts='mpegts udp://192.168.178.169:8000/', capture=True)



