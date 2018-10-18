
import sys, random, json, os
from halibot import HalModule

class Emote(HalModule):

	HAL_MINIMUM = "0.2.0"

	def init(self):
		# Emotes are of type <string, string[]>
		self.emotes = {}

		self.path = self.config.get('emote-path')
		if self.path is None:
			self.path = 'emotes.json'

		self.type = self.config.get('emote-type')
		if self.type is None:
			self.type = 'random'

		self.log.info('using emotes path: ' + self.path)

		try:
			if not os.path.isfile(self.path):
				with open(self.path, 'w+') as f:
					json.dump(self.emotes, f)

			else:
				with open(self.path, 'r') as f:
					self.emotes = json.loads(f.read())

		except (ValueError):
			self.log.error('Couldn\'t parse JSON: ', file=sys.stderr)
		except (IOError, OSError):
			self.log.error('Couldn\'t open emotes file: ', file=sys.stderr)


	def emote(self, pattern=""):
		if pattern not in self.emotes:
			return 'Emote not found :('
		else:
			if self.type == 'random':
				return random.choice(self.emotes[pattern])
			elif self.type == 'queue':
				retEmote = self.emotes[pattern].pop()
				self.emotes[pattern].insert(0, retEmote)
				return retEmote

	def emoteadd(self, emote):
		args = emote.split(' ', 1)

		if args[0] not in self.emotes:
			self.emotes[args[0]] = [args[1]]
		else:
			self.emotes[args[0]].append(args[1])

		with open(self.path, 'w') as f:
			json.dump(self.emotes, f)

		return 'Emote "' + args[0] + '" added :)'

	def emotelist(self):
		if len(self.emotes) < 1:
			return 'No emotes currently stored :('
		else:
			return 'Emotes: ' + ', '.join(list(self.emotes.keys()))

	def emotedel(self, emote):
		if emote in self.emotes:
			del self.emotes[emote]

			with open(self.path, 'w') as f:
				json.dump(self.emotes, f)

			return 'You strike down the legendary "' + emote + '" with your mighty sword.'
		else:
			return 'You swing your sword but strike only the wind.'

	def receive(self, msg):
		ls = msg.body.split(' ')
		cmd = ls[0] if len(ls) > 0 else ''
		arg = ' '.join(ls[1:]).strip() if len(ls) > 1 else ''

		if cmd == '!lenny':
			self.reply(msg, body='( ͡° ͜ʖ ͡°)')
		elif cmd == '!emoteadd':
			self.reply(msg, body=self.emoteadd(arg))
		elif cmd == '!emotelist':
			self.reply(msg, body=self.emotelist())
		elif cmd == '!emotedel':
			self.reply(msg, body=self.emotedel(arg))
		elif cmd == '!emote':
			self.reply(msg, body=self.emote(pattern=arg))

