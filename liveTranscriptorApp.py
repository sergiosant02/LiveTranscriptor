import kivy
kivy.require("2.3.1")

from kivy.app import App
from kivy.uix.label import Label

from pages.transcriptionPage import TranscriptionPage

class LiveTranscriptorApp(App):

    def build(self):
        return TranscriptionPage()