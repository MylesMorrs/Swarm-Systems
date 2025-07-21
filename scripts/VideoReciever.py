import gi
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def on_message(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-Of-Stream reached.")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        loop.quit()
    elif t == Gst.MessageType.STATE_CHANGED:
        if message.src == pipeline:
            old_state, new_state, pending = message.parse_state_changed()
            if new_state == Gst.State.PLAYING:
                print("Video stream started and window should be visible.")

def main():
    Gst.init(None)

    global pipeline
    pipeline = Gst.parse_launch(
        "udpsrc port=5000 caps=\"application/x-rtp, media=(string)video, encoding-name=(string)H264\" ! "
        "rtph264depay ! "
        "avdec_h264 ! "
        "videoconvert ! "
        "autovideosink"
    )

    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message, loop)

    pipeline.set_state(Gst.State.PLAYING)

    print("Waiting for video stream on UDP port 5000... Press Ctrl+C to stop.")
    try:
        loop.run()
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        pipeline.set_state(Gst.State.NULL)
        print("Receiver stopped.")

if __name__ == "__main__":
    main()
