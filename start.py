import itertools
import re

class Obfuscator:
	def obfuscate(code):
		code = Obfuscator.remove_comments(code)
		# меняем имена классов и функций
		cn = Obfuscator.get_defined_classes(code)
		fn = Obfuscator.get_defined_functions(code)
		objects_and_names = Obfuscator.get_new_names(cn+fn)
		code = Obfuscator.replace_func_names(code, objects_and_names)

		# меняем переменные, объявленные в скобках
		func_parts = Obfuscator.get_func_parts(code)
		for f_name in func_parts:
			old_code = '\n'.join(func_parts[f_name])
			print(old_code)
			new_code_lines = Obfuscator.replace_variables(func_parts[f_name])
			new_code = '\n'.join(new_code_lines)
			print(new_code)
			# code = re.sub(re.compile(old_code), new_code, code)
			code = code.replace(old_code, new_code)

		# удаляем пустые строки
		lines=[x for x in code.splitlines() if x and re.search(r'\w+', x)]
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
		new_names = list((''.join(x) for x in itertools.product('o0O', repeat=5)))
		if len(names) > len(new_names):
			raise Exception
		res={}
		for i in range(len(names)):
			res[names[i]] = new_names[i]
		return res

	def get_new_names_vars(names):
		new_names = list((''.join(x) for x in itertools.product('QcC', repeat=5)))
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
				while i<len(lines) and len(lines[i])>spaces_count and (lines[i][spaces_count:][0] == ' ' or lines[i][spaces_count:][0] == '\t'):
					funcs[m.group(2)].append(lines[i])
					i+=1
			i+=1
		
		return funcs

		# functions = re.findall(regexp, code)
		# not_spec_funcs = [x for x in functions if x[:1]!='__' and x[-2:]!='__']
		# return not_spec_funcs

	def build_functions(funcs):
		# возвр словарь: имя функции и ее код
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
		return res_funcs


	def replace_variables(func_code_lines):
		# print(func_code_lines)
		regexp = re.compile(r'def (.+?)\((.*)\)')
		variables = re.search(regexp, func_code_lines[0]).group(2).split(',')
		variables = [x.strip() for x in variables]
		new_names = Obfuscator.get_new_names_vars(variables)
		res=[]
		for line in func_code_lines: 
			for v in variables:
				m =re.search(r'\W*('+v+r')\W*', line)
				if m:
					line = line.replace(v, new_names[v])
			res.append(line)
		return res








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
	# f_codes = Obfuscator.build_functions(f_parts)
	f_replaced = {}
	for f in f_parts:
		f_replaced[f] = Obfuscator.replace_variables(f_parts[f])
	print(f_replaced)
	for f in f_replaced:
		code = code.replace()
	# ====================


	# print([i for i in itertools.permutations('oO0', 3)])
	# print([''.join(i) for i in itertools.product('oO0', repeat=3)])



