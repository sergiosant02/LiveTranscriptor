from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from typing import List

from providers.models_provider import ModelProvider
from providers.device_provider import DeviceProvider
from providers.transcriptor import Transcriptor

class TranscriptionPage(GridLayout):
    
    model_name: str | None = None
    device_index: int | None = None
    transcriptor: Transcriptor = None
    transriptions: List | None = None
    
    
    def __init__(self, **kwargs):
        super(TranscriptionPage, self).__init__(**kwargs)
        self.rows = 4
        self.models_drop_down = DropDown()
        self.audio_device_drop_down = DropDown()
        self.control_button = Button(text="Start", disabled=True, size=(Window.width, 40), on_release=lambda btn: self.on_control_button_click(), background_color=(0,1,0,1))
        self.define_selectors()
        self.define_models_options()
        self.define_audio_device_options()
        self.add_widget(self.control_button)
        self.first_text_label = Label(text="Select the model and the device before to start")
        self.add_widget(self.first_text_label)
        self.transcriptor = Transcriptor()
        self.transriptions = ["", ""]
        
    def select_option_action(self, btn, drop, value, model, opt):
        drop.select(value)
        btn.text = model
        match(opt):
            case 0:
                self.model_name = value
            case 1:
                print("----"*10,value, "----"*10)
                self.device_index = value
                self.transcriptor.device_id = value
                
        self.check_start_button_restrictions()
                
        
    def define_models_options(self):
        self.select_model_button.bind(on_release=self.models_drop_down.open)
        for index, model in enumerate(ModelProvider.get_available_models()):
            btn = Button(text=model, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn=btn, model=model, i=index: self.select_option_action(self.select_model_button, self.models_drop_down, model, model, 0))
            self.models_drop_down.add_widget(btn)
            
    def define_audio_device_options(self):
        self.select_audio_device_button.bind(on_release=self.audio_device_drop_down.open)
        for index, name in DeviceProvider.get_available_devices():
            btn = Button(text=name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn=btn, name=name, i=index: self.select_option_action(self.select_audio_device_button, self.audio_device_drop_down, i, name, 1))
            self.audio_device_drop_down.add_widget(btn)

    
    def define_selectors(self):
        self.selectors_col_group = GridLayout()
        self.selectors_col_group.cols = 2
        self.select_model_button = Button(text="Select model", size_hint=(None, None), size=(Window.width//2,40))
        self.selectors_col_group.add_widget(self.select_model_button)
        
        self.select_audio_device_button = Button(text="Select audio device", size_hint=(None, None), size=(Window.width//2,40))
        self.selectors_col_group.add_widget(self.select_audio_device_button)
        self.add_widget(self.selectors_col_group)
        
    def check_start_button_restrictions(self):
        self.control_button.disabled = not (self.model_name != None and self.device_index != None)
        
    def on_control_button_click(self):
        if self.transcriptor.working:
            self.control_button.text = "Start"
            self.control_button.background_color = (0, 1, 0, 1)
            self.transcriptor.stop()
        else: 
            self.control_button.text = "Stop"
            self.control_button.background_color = (1, 0, 0, 1)
            self.transcriptor.start(fn=self.represent_transcription, device=self.device_index, model_size=self.model_name)
            
    def represent_transcription(self, text):
        self.transriptions.append(text)
        self.transriptions = self.transriptions[:-2]
        self.first_text_label.text = text
        #self.second_text_label.text = self.transriptions[1]