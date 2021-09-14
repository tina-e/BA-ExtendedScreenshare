# Extended Screenshare
<img width="50%" alt="icon" src="img/icon.png" allign="center">

Extended Screenshare is a Screensharing-Tool to improve collaborative work.
This tool allows you to choose the shared region freely by your self
instead of sharing the entire screen or a single application.
As the receiving part, you can interact with the stream and even drag-and-drop file through it.
Content which is pasted in the clipboard is accessible for both parts.

## Install the application
1. Install the following programs via `sudo apt install`:
   - sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
   - ...
   - ...
2. Use `pip install -r requirements.txt` (or maybe `pip3`) to install the necessary packages.

## Run the application
1. As the streaming part, make sure you have reading and writing permission for `/dev/uinput`.
To do this: `sudo chmod a+rw /dev/uinput`
2. Use `evtest` and `xinput` list to find out the event number of you keyboard and mouse device.
Make sure to use the mouse device which is listed as pointer **and** keyboard device.
3. Run `./extended_screenshare.sh` with `-k {your keyboard event number}` and `-m {your mouse event number}`

A tray icon appears. Use the option `Quit` to exit the application.
