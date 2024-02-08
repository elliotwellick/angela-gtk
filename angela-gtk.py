import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import requests
import json

class ChatBotApp(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Angela by Elliot")

        self.set_border_width(10)
        self.set_default_size(400, 300)

        self.donate_button = Gtk.Button(label="Donate")
        self.donate_button.connect("clicked", self.open_donation_dialog)

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.layout.pack_start(self.donate_button, False, False, 0)

        self.chat_history = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.chat_history)
        self.layout.pack_start(self.scroll, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type your message here, Angela is Listening...")
        self.entry.connect("activate", self.send_message)
        self.layout.pack_start(self.entry, False, True, 0)

        self.user_history = []
        self.bot_history = []

        self.add(self.layout)

    def send_message(self, widget):
        message = self.entry.get_text()
        self.user_history.append({"role": "user", "content": message})
        self.entry.set_text("")
        response = self.get_bot_response(message)
        self.bot_history.append({"role": "assistant", "content": response})
        self.display_conversation()

    def open_donation_dialog(self, widget):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK, text="Ohh, Really?? GO, HELP TO THOSE WHO IS IN NEED.")
        dialog.format_secondary_text("I'M RICH!")
        dialog.run()
        dialog.destroy()

    def get_bot_response(self, message):
        url = 'https://xpert-platform-services-api.prod.ai.2u.com/xpert/chat'
        headers = {
            'Host': 'xpert-platform-services-api.prod.ai.2u.com',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.216 Safari/537.36',
            'Referer': 'https://www.edx.org/',
        }
        payload = {
            "message_list": self.user_history,
            "context": {}
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "Error: Something went wrong. Try Restarting Angela."

    def display_conversation(self):
        self.chat_history.set_homogeneous(False)
        self.chat_history.set_spacing(10)
        self.chat_history.set_valign(Gtk.Align.START)

        for child in self.chat_history.get_children():
            self.chat_history.remove(child)

        for user_msg, bot_msg in zip(self.user_history, self.bot_history):
            user_label = Gtk.Label(label=user_msg["content"], wrap=True, xalign=0)
            user_label.set_margin_bottom(5)
            user_label.set_selectable(True)
            self.chat_history.pack_start(user_label, False, False, 0)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            separator.set_margin_bottom(5)
            self.chat_history.pack_start(separator, False, False, 0)

            bot_label = Gtk.Label(label=bot_msg["content"], wrap=True, xalign=1)
            bot_label.set_margin_bottom(5)
            bot_label.set_selectable(True)
            self.chat_history.pack_start(bot_label, False, False, 0)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            separator.set_margin_bottom(5)
            self.chat_history.pack_start(separator, False, False, 0)

        self.show_all()

win = ChatBotApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
