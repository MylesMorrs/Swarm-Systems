import gi
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

def main():
    Gst.init(None)

    # Replace with your Linux receiver IP here:
    receiver_ip = "192.168.1.100"
    video_device = "Integrated Camera"  # Your camera name

    # Build pipeline:
    # Video source: ksvideosrc + convert + encode + payloader + UDP sink
    # Audio source: wasapisrc (Windows default audio capture) + convert + encode + payloader + UDP sink
    # tee video and audio also to local preview sink

    pipeline_desc = f"""
        ksvideosrc device-name="{video_device}" ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! rtph264pay name=pay0 pt=96 ! udpsink host={receiver_ip} port=5000

        wasapisrc ! audioconvert ! audioresample ! opusenc bitrate=64000 ! rtpopuspay name=pay1 pt=97 ! udpsink host={receiver_ip} port=5002

        ksvideosrc device-name="{video_device}" ! videoconvert ! autovideosink sync=false

        wasapisrc ! audioconvert ! autoaudiosink sync=false
    """

    pipeline = Gst.parse_launch(pipeline_desc)
    pipeline.set_state(Gst.State.PLAYING)

    print(f"Streaming video+audio via UDP to {receiver_ip} (video:5000, audio:5002).")
    print("Local preview started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)
        print("Streaming stopped.")

if __name__ == "__main__":
    main()
