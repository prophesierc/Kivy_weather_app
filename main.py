from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from datetime import datetime
import geocoder
import my_api

g = geocoder.ip('me')
Window.size = (350, 580)

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class ImageButton(ButtonBehavior, AsyncImage):
    pass
			
class Main(MDScreen):
    def my_callback(self, dt=0):
        dt = datetime.now()
        self.clock.text = f'{dt.strftime("%A")}  |  {dt.strftime("%b")} {dt.strftime("%d")} | {dt.strftime("%I:%M")}'

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

        #weather icon widget
        img_url = my_api.weather_icon()
        self.aimg = AsyncImage(source=img_url,
                               pos_hint={
                                   'center_x': 0.50,
                                   'center_y': 0.75
                               })
        self.add_widget(self.aimg)

        #description
        self.description = Label(text=my_api.description(),
                                 halign='center',
                                 pos=(0, 50),
                                 font_size='20sp')
        self.add_widget(self.description)

        #city
        self.location = Label(text=f'{g.city}',
                              halign='center',
                              pos=(0, -110),
                              font_size='30sp')
        self.add_widget(self.location)

        #clock date and time
        self.clock = MDLabel(
            pos_hint={
                'center_x': .565,  #1.17,
                'center_y': 0.22
            },
            theme_text_color="Custom",
            text_color='white',
            font_style='H5',
            padding=('1dp', '1dp'),
        )
        self.add_widget(self.clock)
        Clock.schedule_interval(self.my_callback, 1)

        #weather temp lbl
        self.temp = MDLabel(
            text=f'{my_api.weather_temp()} | {my_api.feels_like()}',
            pos_hint={
                'center_x': 0.78,
                'center_y': 0.1
            },
            theme_text_color="Custom",
            text_color='white',
            font_style='H3',
        )
        self.add_widget(self.temp)


class myApp(MDApp):
	def build(self):
		self.sm = ScreenManagement()
		self.sm.add_widget(Main(name='main'))
		self.title = ' '
		self.sm.cols = 1
		self.theme_cls.theme_style = 'Dark'
		return self.sm


#runs kivy GUI
if __name__ == '__main__':
	myApp().run()
