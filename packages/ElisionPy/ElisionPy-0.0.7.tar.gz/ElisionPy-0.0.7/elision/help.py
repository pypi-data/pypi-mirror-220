class help_module:

	stringer_1 = 'Выберите номер пункта из списка\n1. Информация о модуле\n2. Завершить и закрыть\n- '
	info = 'Создатель: Гинджи\nЛицензия: Protect - Внутренняя защита.\nВерсия: v.0.0.1\n\n'
	error_1 = 'Такого номера не существует, возврат...!'

	def __init__(self):
		pass

	@classmethod
	def help(self) -> "Elision Module":
		while True:
			ot = input(self.stringer_1)
			if ot == "1":
				print(self.info)
			elif ot == "2":
				raise SystemExit()
			else:
				print(self.error_1)



if __name__ == "__main__":
	help_module.help()