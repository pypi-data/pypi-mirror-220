class random:

	seed_sleep, seed_a, seed_c = 0.1, 1, 4

	def __init__(self):
		pass

	def int(self, x: int = None, y: int = None) -> None:

		if x > y:
			buf = x
			x = y
			y = buf


		date_now = str(datetime.datetime.now())[-6:]

		int_for_gen = int(date_now + date_now)

		generate = 0

		ei = 0

		while(True):
			if ei <= 40:
				if generate >= x and generate <= y:
					break
				elif x == y:
					return x

				if int_for_gen < x:
					int_for_gen = int_for_gen + y + 25
					ei += 1

				int_for_gen /= 17

				generate = int_for_gen
			else:
				int_for_gen = int_for_gen + y + 26
				ei = 0
		return int(round(generate))

	@classmethod
	def seed(self, a: int = seed_a, c: int = seed_c) -> None:

		if c < 0: c = 0

		elif c > 16: c = 16

		mas: list = []
		for f in range(c):
			g = random.int(self, 1, 9)
			mas.append(g)
			time.sleep(self.seed_sleep)
		status_1 = ''.join(map(str, mas))
		status_2 = f'{a}.{status_1}'
		return float(status_2)

	@classmethod
	def choice(self, l: list = None) -> None:
		list_number_global = len(l)

		randoms = random.int(self, 1, list_number_global)

		return l[randoms - 1]
			
	@classmethod
	def string(self, version: int = 1, listing: list = None) -> None:
		if version == 1:
			list_string: list = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j',' k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']

			random_choice = self.choice(list_string)

			return random_choice
		elif version == 2:
			list_string: list = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j',' k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '_', '-']

			random_choice = self.choice(list_string)

			return random_choice

		elif version == 3:
			if listing != None:
				random_choice = self.choice(listing)

				return random_choice
				
			else:
				print('Для версии 3 требуется ещё параметр "listing"')

		else:
			print('Параметр version может принимать значения 1, 2 или 3')