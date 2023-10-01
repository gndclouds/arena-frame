from kivy.config import Config
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.core.window import Window
import requests

Config.set('graphics', 'fullscreen', 'auto')  # Set the app to fullscreen mode


BASE_URL = "https://api.are.na/v2/channels/"
CHANNEL_ID = 'objects-gt0ewchjpw8'
FULL_URL = BASE_URL + CHANNEL_ID

class ArenaApp(App):

	current_image_index = 0
	image_urls = []
	
	def get_arena_data(self):
		response = requests.get(FULL_URL)
		data = response.json()
		return data
	
	def extract_image_urls(self, data):
		image_urls = []
		
		# Check if 'contents' key exists and is a list.
		if 'contents' in data and isinstance(data['contents'], list):
			for item in data['contents']:
				if 'image' in item and 'square' in item['image'] and 'url' in item['image']['square']:
					url = item['image']['square']['url']
					image_urls.append(url)
		
		return image_urls
	

	def update_image(self, dt):
		self.current_image_index += 1
		if self.current_image_index >= len(self.image_urls):
			self.current_image_index = 0
		self.image_widget.source = self.image_urls[self.current_image_index]

	def build(self):
		data = self.get_arena_data()
		self.image_urls = self.extract_image_urls(data)
		
		if self.image_urls:
			self.image_widget = AsyncImage(
				source=self.image_urls[self.current_image_index],
				size=(Window.width, Window.height),
				size_hint=(None, None),
				allow_stretch=True,
				keep_ratio=True
			)
			Clock.schedule_interval(self.update_image, 60)
			return self.image_widget
		else:
			return Label(text="No images found.")
	
	def on_touch_down(self, touch):
		# Check if left or right of the screen was tapped
		if touch.x < Window.width * 0.3:
			# Left side tapped, show previous image
			self.current_image_index -= 1
			if self.current_image_index < 0:
				self.current_image_index = len(self.image_urls) - 1
		elif touch.x > Window.width * 0.7:
			# Right side tapped, show next image
			self.current_image_index += 1
			if self.current_image_index >= len(self.image_urls):
				self.current_image_index = 0
	
		# Update displayed image
		self.image_widget.source = self.image_urls[self.current_image_index]


ArenaApp().run()
