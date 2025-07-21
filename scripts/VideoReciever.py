import gi
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst

def main():
    Gst.init(None)

    pipeline = Gst.parse_launch(
        "udpsrc port=5000 caps=\"application/x-rtp, media=(string)video, encoding-name=(string)H264\" ! "
        "rtph264depay ! "
        "avdec_h264 ! "
        "videoconvert ! "
        "autovideosink"
    )

    pipeline.set_state(Gst.State.PLAYING)

    print("Receiving video stream on UDP port 5000... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)
        print("Receiver stopped.")

if __name__ == "__main__":
    main()
