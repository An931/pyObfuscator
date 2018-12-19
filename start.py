import itertools
import re

class Obfuscator:
	def obfuscate(page_code):
		pass

	def get_code(path):
		with open(path) as f:
			return f.read()

	def get_defined_functions(code):
		# возвр имена объявленных в коде функций
		regexp = re.compile(r'def (.+?)\(')
		functions = re.findall(regexp, code)
		return functions

	def get_defined_classes(code):
		regexp = re.compile(r'class (.+?)[\(\:]')
		classes = re.findall(regexp, code)
		return classes

	def get_new_names(names):
		new_names = list((''.join(x) for x in itertools.product('oO0', repeat=3)))
		if len(names) > len(new_names):
			raise Exception
		res={}
		for i in range(len(names)):
			res[names[i]] = new_names[i]
		return res

	def replace_func_names_REGEXP(code, func_new_names_dict):
		new_code = code
		for f in func_new_names_dict.keys():
			regexp = re.compile(r'[\s]*('+f+r')\(+')
			print(re.findall(regexp, code))
			new_code = re.sub(regexp, func_new_names_dict[f], new_code)
			print(new_code)
		return new_code

	def replace_func_names(code, names_dict):
		# заменяет в том числе вхождения в название 
		new_code = code
		for f in names_dict.keys():
			regexp = re.compile(r'[\s]*('+f+r')\(+')

			new_code = new_code.replace(f, names_dict[f])
		return new_code

	def replace_class_names():
		pass

	def replace_self(code):
		pass

	def replace_variables(code, names_dict):
		pass


if __name__ == '__main__':
	# code = Obfuscator.get_code('rectangle.py')
	# fs = Obfuscator.get_defined_functions(code)
	# f_and_names = Obfuscator.get_new_funcnames(fs)
	# print(f_and_names)
	# new_code = Obfuscator.replace_func_names(code, f_and_names)
	# print(new_code)

	code = Obfuscator.get_code('rectangle.py')
	fs = Obfuscator.get_defined_classes(code)
	ff = Obfuscator.get_defined_functions(code)
	f_and_names = Obfuscator.get_new_names(fs+ff)
	print(f_and_names)
	new_code = Obfuscator.replace_func_names(code, f_and_names)
	print(new_code)

	# print([i for i in itertools.permutations('oO0', 3)])
	# print([''.join(i) for i in itertools.product('oO0', repeat=3)])


# -----------------
# убрать комменты
# переименовать функции, классы, селфы
# переименовать локальные переменные в функциях (в том числе селфы)
