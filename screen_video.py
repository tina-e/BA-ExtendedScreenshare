# ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 output.mp4
#                    breite x hoehe                             startpunkt

# http://morrillplou.me/blog/index.php/2019/03/04/streaming-video-over-lan-with-ffmpeg/
# !!! use IP of accessing device not streming device !!!
# streaming: ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 -preset ultrafast -tune zerolatency -codec libx264 -f mpegts udp://192.168.178.169:8000/
# streaming: ffmpeg -video_size 1024x768 -framerate 25 -f x11grab mpegts udp://192.168.178.169:8000/ -i :0.0+100,200
# accessing: ffplay -f mpegts udp://192.168.178.136:8000
import subprocess
import threading
import ffmpeg

x_pos = 100
y_pos = 100
width = 1500
height = 750
ip_receiver = '192.168.178.136'
port = 9000

def start_stream():
    subprocess.Popen(f"ffmpeg -video_size {width}x{height} -framerate 25 -f x11grab -i :0.0+{x_pos},{y_pos} -f mpegts udp://{ip_receiver}:{port}", shell=True)


def start_stream_bindings():
    (
        ffmpeg
            .input(f':0.0+{x_pos},{y_pos}', format='x11grab', framerate=25, s='{}x{}'.format(width, height))
            .output(f'udp://{ip_receiver}:{port}/', format='mpegts')
            # .output(f'udp://{ip_receiver}:{port}/', format='mpegts', preset='ultrafast', tune='zerolatency')
            .run()
    )


def access_stream():
    subprocess.check_output(f"ffplay -f mpegts udp://{ip_receiver}:{port}/", shell=True)


threading.Thread(target=start_stream_bindings).start()
threading.Thread(target=access_stream).start()

# !!! dont re-run, stop !!!

# ohne low latency mit ffplay bindings: 5.93
# mit low latency mit ffplay bindings: 8.64
# ohne low latency ohne ffplay bindings: 5.62
# mit low latency ohne ffplay bindings: 5.59
# -> ohne ffplay bindings


# scheint langsamer zu sein -> shell nutzen
# https://stackoverflow.com/questions/59611075/how-would-i-go-about-playing-a-video-stream-with-ffpyplayer
def access_stream_bindings():
    from ffpyplayer.player import MediaPlayer
    import numpy as np
    import cv2

    player = MediaPlayer(f"udp://{ip_receiver}:{port}/")
    val = ''
    while val != 'eof':
        frame, val = player.get_frame()
        if val != 'eof' and frame is not None:
            img, t = frame
            w = img.get_size()[0]
            h = img.get_size()[1]
            arr = np.uint8(np.asarray(list(img.to_bytearray()[0])).reshape(h, w, 3))  # h - height of frame, w - width of frame, 3 - number of channels in frame
            cv2.imshow('test', arr)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

# https://pypi.org/project/python-ffmpeg-video-streaming/
# import ffmpeg_streaming
# capture = ffmpeg_streaming.input(':0.0+100,200', capture=True)

# ffmpeg -f x11grab -r 1 -loglevel panic -s `xdpyinfo | grep 'dimensions:'|awk '{print $2}'` -i $DISPLAY -qscale 0 -f mpegts udp://localhost