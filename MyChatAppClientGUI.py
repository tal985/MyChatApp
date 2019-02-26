import kivy, socket, sys, threading
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
Config.set('graphics', 'multisamples', '0') 
from kivy.utils import get_color_from_hex

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = "GUI"
ip = "127.0.0.1"
port = 5000

Builder.load_string("""
#:import get_color_from_hex __main__.get_color_from_hex
<Chat>:
    GridLayout:
        rows: 2
        
        GridLayout:
            cols: 1
            rows: 0
            ScrollView:
                size: self.size
                do_scroll_x: False
                Label:
                    id: msg_log
                    text_size: self.width,None
                    size_hint_y: None
                    height: self.texture_size[1]
                    font_size: root.height / 20
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 15
            canvas:
                Color:
                    rgba: (0.746,0.8,0.86,1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            TextInput:
                id: message
                hint_text: "Type here"
                multiline: False
                on_text_validate: root.sendMsg(message.text)
""")

class Chat(Screen):
    global client
    def __init__(self,**kwargs):
        super(Chat,self).__init__(**kwargs)
        self.msg_log = self.ids["msg_log"]
        
    def on_enter(self):
        try:
            client.connect((ip, port))
        except Exception as e:
            print(e)
            exit()
        client.send(name.encode())

        iThread = threading.Thread(target = self.handleData)
        iThread.daemon = True
        iThread.start()

    def sendMsg(self, msg):
        try:
            client.send(bytes(msg, "utf-8"))
        except Exception as e:
            print(e)

    def handleData(self):
        while True:
            try:
                data = client.recv(1024)
                self.msg_log.text += str(data, "utf-8") + "\n"
            except Exception as e:
                print(e)

class MyChatAppClientGUI(App):
    def build(self):
        return sm

sm = ScreenManager()

sm.add_widget(Chat(name = "main_screen"))

if __name__ == "__main__":
    MyChatAppClientGUI().run()