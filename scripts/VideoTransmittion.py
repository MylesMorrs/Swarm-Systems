import gi
import signal

gi.require_version('Gst', '1.0')
from gi.repository import Gst

def main():
    Gst.init(None)

    pipeline = Gst.parse_launch(
        "v4l2src device=/dev/video0 ! "
        "videoconvert ! "
        "x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! "
        "rtph264pay ! "
        "udpsink host=192.168.1.100 port=5000"
    )

    pipeline.set_state(Gst.State.PLAYING)

    print("Streaming video via UDP... Press Ctrl+C to stop.")
    try:
        signal.pause()
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)
        print("Streaming stopped.")

if __name__ == "__main__":
    main()
