import itertools
import re

class Obfuscator:
	def obfuscate(code):
		code = Obfuscator.remove_comments(code)
		# меняем имена классов
		cn = Obfuscator.get_defined_classes(code)
		fn = Obfuscator.get_defined_functions(code)
		objects_and_names = Obfuscator.get_new_names(cn+fn)
		code = Obfuscator.replace_func_names(code, objects_and_names)
		lines=[x for x in code.splitlines() if x]
		return '\n'.join(lines)

	def get_code(path):
		with open(path) as f:
			return f.read()

	def get_defined_functions(code):
		# возвр имена объявленных в коде функций
		regexp = re.compile(r'def (.+?)\(')
		functions = re.findall(regexp, code)
		not_spec_funcs = [x for x in functions if x[:1]!='__' and x[-2:]!='__']
		return not_spec_funcs

	def get_defined_classes(code):
		regexp = re.compile(r'class (.+?)[\(\:]')
		classes = re.findall(regexp, code)
		return classes

	def remove_comments(code):
		regexp_single = re.compile(r'#.*')
		code = re.sub(regexp_single, '', code)
		regexp_few_lines = re.compile(r'\'\'\'.*\'\'\'', re.DOTALL)
		code = re.sub(regexp_few_lines, '', code)
		return code

	def get_new_names(names):
		new_names = list((''.join(x) for x in itertools.product('oO0', repeat=3)))
		if len(names) > len(new_names):
			raise Exception
		res={}
		for i in range(len(names)):
			res[names[i]] = new_names[i]
		return res

	def replace_func_names(code, names_dict):
		# заменяет в том числе вхождения в название 
		new_code = code
		for f in names_dict.keys():
			regexp = re.compile(r'[\s]*('+f+r')\(+')

			new_code = new_code.replace(f, names_dict[f])
		return new_code

	def replace_class_names(code, names_dict):
		new_code = code
		for f in names_dict.keys():
			regexp = re.compile(r'[\s]*('+f+r')\(+')

			new_code = new_code.replace(f, names_dict[f])
		return new_code

	def replace_variables(code, names_dict):
		pass

	def get_func_parts(code):
		# возвр участки кода- функции для выведения лок переменных
		lines = code.splitlines()
		regexp = re.compile(r'([\s]*)def (.+?)\(')
		funcs = {}
		i=0
		while i < len(lines):
			m = re.search(regexp, lines[i])
			if m:
				spaces_count=len(m.group(1))
				funcs[m.group(2)] = [lines[i]]
				i+=1
				while lines[i][spaces_count:][0] == ' ' or lines[i][spaces_count:][0] == '\t':
					funcs[m.group(2)].append(lines[i])
					i+=1
			i+=1
		
		return funcs

		# functions = re.findall(regexp, code)
		# not_spec_funcs = [x for x in functions if x[:1]!='__' and x[-2:]!='__']
		# return not_spec_funcs

	def build_functions(funcs):
		# возвр словарь: имя функции и ее локальные переменные
		# funcs - словарь: имя и список строк
		def get_spaces(line):
			i, res=0, ''
			while line[i] in [' ', '\t']:
				res+=line[i]
				i+=1
			return res
		res_funcs={}
		for name in funcs:
			func_list = funcs[name]
			# func_list.append(get_spaces(func_list[1])+'LOCALS=locals()')
			progr_code = '\n'.join(func_list)
			res_funcs[name] = progr_code
			exec(progr_code)
		return res_funcs

	def replace_variablebles(func):
		pass



if __name__ == '__main__':
	# code = Obfuscator.get_code('rectangle.py')
	# fs = Obfuscator.get_defined_functions(code)
	# f_and_names = Obfuscator.get_new_funcnames(fs)
	# print(f_and_names)
	# new_code = Obfuscator.replace_func_names(code, f_and_names)
	# print(new_code)

	code = Obfuscator.get_code('rectangle.py')
	# fs = Obfuscator.get_defined_classes(code)
	# ff = Obfuscator.get_defined_functions(code)
	# f_and_names = Obfuscator.get_new_names(fs+ff)
	# print(f_and_names)
	# new_code = Obfuscator.replace_func_names(code, f_and_names)
	# print(new_code)
	f_parts = Obfuscator.get_func_parts(code)
	f_codes = Obfuscator.build_functions(f_parts)
	print(f_codes)
	# ====================


	# print([i for i in itertools.permutations('oO0', 3)])
	# print([''.join(i) for i in itertools.product('oO0', repeat=3)])



