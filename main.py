from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
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


# Splash screeen
class Splash(MDScreen):
	def __init__(self, **kwargs):
		super(Splash, self).__init__(**kwargs)

        # API label
		self.api_lbl = Label(text='[b]Enter your OpenWeatherMap API key[/b]',
                             size_hint=(.5, .3),
                             pos_hint={
                                 'center_x': .5,
                                 'center_y': .9
                             },
                             markup=True)

        #api_key text input box
		self.api_text = MDTextField(text='',
            pos_hint={
                'center_x': 0.5,
                'center_y': 0.6
            },
            size_hint={.5, .07},
            halign='center',
            hint_text='OpenWeatherMap API Key',
            multiline=False,
        )

        #api button to enter api key
		self.api_btn = Button(text='Enter',
                              size_hint=(.5, .07),
                              pos_hint={
                                  'center_x': .5,
                                  'center_y': .5
                              })

        ##api_key error flow control
		self.null_text_value = MDTextField(
			pos_hint={
                'center_x': 0.5,
                'center_y': 0.6
            },
            size_hint={.5, .07},
            halign='center',
            hint_text='OpenWeatherMap API Key',
            multiline=False,
			required = True
        )
        
		self.add_widget(self.api_lbl)
		self.add_widget(self.api_text)
		self.add_widget(self.api_btn)
		self.api_btn.bind(on_press=self.changer)	
		# intregrate API KEY
		#my_api.api_key = self.api_text.text

	def changer(self, *args, **kwargs):
		if len(self.null_text_value.text) > 0 :
			if my_api.response.status_code == '200':
				self.manager.current = 'main'
		else:
			self.remove_widget(self.api_text)
			self.remove_widget(self.null_text_value)
			self.add_widget(self.null_text_value)
				

class Main(MDScreen):
    def my_callback(self, dt=0):
        dt = datetime.now()
        self.clock.text = f'{dt.strftime("%A")}  |  {dt.strftime("%b")} {dt.strftime("%d")} | {dt.strftime("%I:%M:%S")}'

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
    def on_start(self):
        self.sm.current = "splash"

    def build(self):
        self.sm = ScreenManagement(transition=FadeTransition())
        self.sm.add_widget(Splash(name="splash"))
        self.sm.add_widget(Main(name='main'))
        self.title = ' '
        self.sm.cols = 1
        self.theme_cls.theme_style = 'Dark'
        return self.sm


#runs kivy GUI
if __name__ == '__main__':
    myApp().run()