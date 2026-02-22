#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gtk, Gdk, Gst, GLib
import os

Gst.init(None)

MEDIA_DIR = "/home/ritwix/Downloads/Redundant/media"
SIZE = 140  # change this to resize


class Sprite(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("floater-sprite")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(SIZE, SIZE)
        self.set_opacity(0.4)

        # Transparent background
        css = Gtk.CssProvider()
        css.load_from_data(b"""
        window {
            background: transparent;
        }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Picture widget
        self.picture = Gtk.Picture()
        self.picture.set_size_request(SIZE, SIZE)
        self.picture.set_hexpand(True)
        self.picture.set_vexpand(True)
        self.set_child(self.picture)

        # Load media files
        self.media_files = [
            os.path.join(MEDIA_DIR, f)
            for f in os.listdir(MEDIA_DIR)
            if f.endswith((".gif", ".mp4", ".webm"))
        ]

        if not self.media_files:
            raise RuntimeError("No media files found in MEDIA_DIR")

        self.index = 0

        # GStreamer player
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.playback_rate = 1.0

        sink = Gst.ElementFactory.make("gtk4paintablesink", "sink")
        if not sink:
            raise RuntimeError(
                "gtk4paintablesink not available. Install gstreamer1-plugin-gtk4"
            )

        self.player.set_property("video-sink", sink)

        paintable = sink.get_property("paintable")
        self.picture.set_paintable(paintable)

        self.player.set_property("uri", self.get_uri())

        # Loop handling
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.player.set_state(Gst.State.PLAYING)

        # Keyboard controller
        controller = Gtk.EventControllerKey()
        controller.connect("key-pressed", self.on_key)
        self.add_controller(controller)

        # Focus opacity change
        self.connect("notify::is-active", self.on_focus_change)

    # ----------------------
    # Media helpers
    # ----------------------

    def get_uri(self):
        path = os.path.abspath(self.media_files[self.index])
        return GLib.filename_to_uri(path)

    def next_media(self):
        self.index = (self.index + 1) % len(self.media_files)
        self.player.set_state(Gst.State.NULL)
        self.player.set_property("uri", self.get_uri())
        self.player.set_state(Gst.State.PLAYING)

    def prev_media(self):
        self.index = (self.index - 1) % len(self.media_files)
        self.player.set_state(Gst.State.NULL)
        self.player.set_property("uri", self.get_uri())
        self.player.set_state(Gst.State.PLAYING)

    # ----------------------
    # Playback speed
    # ----------------------

    def set_playback_rate(self, rate):
        self.playback_rate = max(0.25, min(3.0, rate))

        success = self.player.seek(
            self.playback_rate,
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
            Gst.SeekType.SET, 0,
            Gst.SeekType.NONE, Gst.CLOCK_TIME_NONE
        )

        print("Playback rate:", self.playback_rate, "Success:", success)

    # ----------------------
    # Bus message handler
    # ----------------------

    def on_message(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self.player.seek_simple(
                Gst.Format.TIME,
                Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                0
            )

    # ----------------------
    # Focus behavior
    # ----------------------

    def on_focus_change(self, *args):
        if self.is_active():
            self.set_opacity(0.6)
        else:
            self.set_opacity(0.9)

    # ----------------------
    # Key controls
    # ----------------------

    def on_key(self, controller, keyval, keycode, state):
        key = Gdk.keyval_name(keyval)

        if key == "space":
            current = self.player.get_state(0).state
            if current == Gst.State.PLAYING:
                self.player.set_state(Gst.State.PAUSED)
            else:
                self.player.set_state(Gst.State.PLAYING)

        elif key == "Right":
            self.next_media()

        elif key == "Left":
            self.prev_media()

        elif key == "Up":
            self.set_playback_rate(self.playback_rate + 0.25)

        elif key == "Down":
            self.set_playback_rate(self.playback_rate - 0.25)

        elif key == "Escape":
            self.close()

        return True


class App(Gtk.Application):
    def do_activate(self):
        win = Sprite(self)
        win.present()


app = App()
app.run()
