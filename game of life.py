__author__ = 'Alexis'

import libtcodpy as libtcod

class Game:
	"""main game app"""


	def __init__(self):
		self.name = b'Game of Life'
		self.font = b'terminal8x8_gs_ro.png'
		self.font_type = libtcod.FONT_TYPE_GREYSCALE
		self.font_layout = libtcod.FONT_LAYOUT_ASCII_INROW
		self.width = 128
		self.height = 72
		self.world = libtcod.console_new(self.width, self.height)
		self.key = libtcod.Key()
		self.mouse = libtcod.Mouse()
		self.matrix = {}
		self.cloud = {}
		self.paradise = []
		self.hell = []
		self.cleaned = []
		self.dying = []
		self.living = 0
		self.dead = 0
		self.generation = 0


	def create(self):
		"""runs the game and opens main console"""
		self.initialize()

		self.gods_words()

		close = False

		while not close:
			# game main loop
			libtcod.console_clear(0)
			self.draw_grid()
			close = self.gods_touch()
			if close:
				break
			self.free_will()


	def initialize(self):
		"""boot window"""
		libtcod.console_set_custom_font(self.font, self.font_type | self.font_layout)
		libtcod.console_init_root(self.width, self.height, self.name, False)


	def gods_touch(self):
		""" player input """

		self.key.vk = libtcod.KEY_NONE

		while self.key.vk is not libtcod.KEY_ENTER:

			libtcod.console_set_default_foreground(0, libtcod.darkest_grey)

			x, y = self.mouse.cx, self.mouse.cy
			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.key, self.mouse)

			if self.mouse.lbutton:
				libtcod.console_set_default_foreground(self.world, libtcod.white)
				libtcod.console_put_char(self.world, x, y, 219)
				libtcod.console_set_default_foreground(0, libtcod.white)
				self.matrix[x, y] = 1
				self.paradise.append((x, y))

			elif self.mouse.rbutton:
				libtcod.console_set_default_foreground(self.world, libtcod.darkest_grey)
				libtcod.console_put_char(self.world, x, y, 224)
				self.matrix[x, y] = 0
				try:
					self.paradise.remove((x, y))
				except:
					pass

			libtcod.console_blit(self.world, 0, 0, self.width, self.height, 0, 0, 0)

			libtcod.console_put_char(0, x, y, 219)

			self.living = len(set(self.paradise))

			self.gods_knowledge(mouse=True)

			libtcod.console_flush()

			if self.key.vk == libtcod.KEY_ESCAPE:
				return True

		self.paradise = list(set(self.paradise))
		self.cloud = dict(self.matrix)


	def gods_words(self):
		"""welcome screen"""
		words = "The Game of Life\n\n" \
		        "l-click / r-click to place / remove seeds\n" \
		        "press enter to observe or reset\n" \
		        "press escape to exit\n\n" \
		        "press any key to start"
		libtcod.console_print_ex(0, self.width // 2, self.height // 2, libtcod.BKGND_NONE, libtcod.CENTER, words)
		libtcod.console_flush()
		libtcod.console_wait_for_keypress(flush=True)


	def draw_grid(self):
		""" draw a grey grid on the console and reset the matrix """
		libtcod.console_clear(self.world)
		libtcod.console_set_default_foreground(self.world, libtcod.darkest_grey)

		x, y = 0, 0

		while y < self.height:
			while x < self.width:
				libtcod.console_put_char(self.world, x, y, 224, libtcod.BKGND_NONE)
				self.matrix[x, y] = 0
				x += 1
			x = 0
			y += 1

		self.paradise.clear()
		self.hell.clear()
		self.dead = 0
		self.living = 0
		self.generation = 0

		libtcod.console_blit(self.world, 0, 0, self.width, self.height, 0, 0, 0)
		libtcod.console_flush()


	def gods_knowledge(self, mouse=False):
		"""add info on the console"""

		fps = libtcod.sys_get_fps()

		knowledge = ("Generation: " + str(self.generation) + " Living: " + str(self.living) +
		             " Dead: " + str(self.dead) + " FPS: " + str(fps))

		if mouse:
			mx, my = self.mouse.cx, self.mouse.cy
			knowledge = [knowledge + " mx: " + str(mx) + " my: " + str(my)]
			knowledge = ("").join(knowledge)

		libtcod.console_set_default_foreground(0, libtcod.white)
		libtcod.console_print_ex(0, 0, self.height-1, libtcod.BKGND_NONE, libtcod.LEFT,knowledge)


	def free_will(self):
		"""second attempt"""

		self.key.vk = libtcod.KEY_NONE

		while self.key.vk is not libtcod.KEY_ENTER:

			self.generation += 1
			self.living = len(self.paradise)

			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, self.key, self.mouse)

			for cell in self.paradise:

				X, Y = cell
				x, y = X-1, Y-1

				while y < Y+2:
					while x < X+2:

						dx, dy = x, y
						if dx < 0:
							dx = self.width-1
						elif dx > self.width-1:
							dx = 0
						if dy < 0:
							dy = self.height-1
						elif dy > self.height-1:
							dy = 0

						if not (dx, dy) in self.cleaned:

							self.cleaned.append((dx, dy))

							a, b = dx-1, dy-1

							total = 0

							while b < dy+2:
								while a < dx+2:

									da, db = a, b
									if da < 0:
										da = self.width-1
									elif da > self.width-1:
										da = 0
									if db < 0:
										db = self.height-1
									elif db > self.height-1:
										db = 0

									total += self.matrix[da, db]

									a += 1

								a = dx-1
								b += 1

							if total == 3:
								self.hell.append((dx, dy))
								self.cloud[dx, dy] = 1

								libtcod.console_set_default_foreground(self.world, libtcod.white)
								libtcod.console_put_char(self.world, dx, dy, 219)

							elif total == 4:
								if (dx, dy) in self.paradise:
									self.hell.append((dx, dy))

							else:
								if (dx, dy) in self.paradise:
									try:
										self.hell.remove((dx, dy))
									except:
										pass

									self.dying.append((dx, dy))
									self.cloud[dx, dy] = 0

									libtcod.console_set_default_foreground(self.world, libtcod.darkest_grey)
									libtcod.console_put_char(self.world, dx, dy, 224)

						x += 1

					x = X-1
					y += 1

			self.dead += len(set(self.dying))
			self.dying.clear()

			self.matrix = dict(self.cloud)

			self.paradise = list(set(self.hell))
			self.hell.clear()

			self.cleaned.clear()

			libtcod.console_blit(self.world, 0, 0, self.width, self.height, 0, 0, 0)

			self.gods_knowledge()

			libtcod.console_flush()


# game launch
libtcod.sys_set_fps(20)
life = Game()
life.create()