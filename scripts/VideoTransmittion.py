import gi
import signal

gi.require_version('Gst', '1.0')
from gi.repository import Gst

def main():
    Gst.init(None)

    pipeline = Gst.parse_launch(
        "v4l2src device=/dev/video0 ! "
        "videoconvert ! "
        "tee name=t "
        "t. ! queue ! x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! rtph264pay ! udpsink host=127.0.0.1 port=5000 "
        "t. ! queue ! autovideosink"
    )

    pipeline.set_state(Gst.State.PLAYING)

    print("Streaming and displaying video... Press Ctrl+C to stop.")
    try:
        signal.pause()
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)
        print("Streaming stopped.")

if __name__ == "__main__":
    main()
