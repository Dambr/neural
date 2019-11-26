import json
import sys
from random import randint as rand
from NeuralNet import *

def parser(fileName):
	f = open(fileName, 'r')
	data = f.read().strip().split('\n')
	while '' in data:
		data.remove('')
	array = list()
	ev = list()
	for i in range(len(data)):
		data[i] = data[i].split('=>')
	for i in range(len(data)):
		for j in range(len(data[i])):
			data[i][j] = data[i][j].strip()
			data[i][j] = data[i][j].replace('{', '[')
			data[i][j] = data[i][j].replace('}', ']')
	for i in range(len(data)):
		array.append(eval(data[i][0]))
		ev.append(eval(data[i][1]))
		if len(eval(data[i][0])) != len(eval(data[i][1])):
			print('Несоответствие длин массива и оценок в строке', i + 1)
			return False
	f.close()
	return [array, ev]

def intInput(string):
	while True:
		try:
			x = int(input(string))
			return x
		except:
			print('Ошибка ввода')

def valueInput(phrase):
	while True:
		value = intInput(phrase)
		if value == 0 or value == 1:
			return value
		else:
			print('Недопустимая оценка')

def writeToFile(fileName, arrayToFile, evalToFile):
	try:
		f = open(fileName, 'a')
	except:
		print('Ошибка открытия файла с известными значениями')
		sys.exit()

	f.write('\n')
	f.write('{')
	for i in range(len(arrayToFile)):
		f.write(str(arrayToFile[i]) + ', ') if i < len(arrayToFile) - 1 else f.write(str(arrayToFile[i]))
	f.write('} => {')
	for i in range(len(evalToFile)):
		f.write(str(evalToFile[i]) + ', ') if i < len(arrayToFile) - 1 else f.write(str(evalToFile[i]))
	f.write('}')
	f.close()


if len(sys.argv) > 2:
	print('Неверное число аргументов запуска программы')
	
elif len(sys.argv) == 1:
	
	neural = neural(2)
	la =  0.01
	T = list()

	try:
		data = parser('data.txt')

	except:
		print('Ошибка открытия файла c известными значениями')
		sys.exit()
	try:
		# Если в data записан False, завершаем работу
		if data == False:
			sys.exit()

		for i in range(len(data[0])):
			for j in range(len(data[0][i])):
				T.append([data[0][i][j], data[1][i][j]])
		
		neural.learning(la, T)
	except:
		print('Данные в файле повреждены')
		sys.exit()

	while True:
		arg1 = intInput('Первый аргумент = ')
		arg2 = intInput('Второй аргумент = ')

		print('Оценка сети =', neural.sign([arg1, arg2]))

		if input('Продолжить? (Y) ') != 'Y':
			break
else:
	if sys.argv[1] == 'first':
		arrayToFile = list()
		evalToFile = list()
		while True:
			arg1 = intInput('Первый аргумент = ')
			arg2 = intInput('Второй аргумент = ')
			ev = valueInput('Оценка = ')
			arrayToFile.append([arg1, arg2])
			evalToFile.append(ev)
			

			if input('Продолжить? (Y) ') != 'Y':
				writeToFile('data.txt', arrayToFile, evalToFile)
				break


	elif sys.argv[1] == 'second':
		while True:
			length = intInput('Длина массива для оценки = ')
			while length < 1:
				length = intInput('Длина массива для оценки = ')
				
			arg1 = intInput('Первая граница генератора случайных чисел = ')
			arg2 = intInput('Вторая граница генератора случайных чисел = ')
			
			
			array = list()
			ev = list()
			for i in range(length):
				array.append([rand(min(arg1, arg2), max(arg1, arg2)), rand(min(arg1, arg2), max(arg1, arg2))])
			for i in range(length):
				_ev = valueInput('Оценка ' + str(array[i]) + ' = ')
				ev.append(_ev)

			writeToFile('data.txt', array, ev)

			if input('Продолжить? (Y) ') != 'Y':
				break

	elif sys.argv[1] == 'third':
		neural = neural(2)
		isWritable = True
		while isWritable:
			
			la =  0.01
			T = list()

			try:
				data = parser('data.txt')

			except:
				print('Ошибка открытия файла с известными значениями')
				sys.exit()
			try:
				# Если в data записан False, завершаем работу
				if data == False:
					sys.exit()

				for i in range(len(data[0])):
					for j in range(len(data[0][i])):
						T.append([data[0][i][j], data[1][i][j]])
				
				neural.learning(la, T)
			except:
				print('Данные в файле повреждены')
				sys.exit()

			length = intInput('Длина массива для оценки = ')
			while length < 1:
				length = intInput('Длина массива для оценки = ')

			arg1 = intInput('Первая граница генератора случайных чисел = ')
			arg2 = intInput('Вторая граница генератора случайных чисел = ')			
			array = list()
			ev = list()
			
			for i in range(length):
				if isWritable == False:
					break
				couple = [rand(min(arg1, arg2), max(arg1, arg2)), rand(min(arg1, arg2), max(arg1, arg2))]
				count = 0
				while neural.sign(couple) == 0:
					couple = [rand(min(arg1, arg2), max(arg1, arg2)), rand(min(arg1, arg2), max(arg1, arg2))]
					count += 1
					if count == 100:
						print('В заданном диапазоне не удается подобрать \"удачные\" пары чисел')
						isWritable = False
						break
				if isWritable:
					array.append(couple)
					_ev = 1
					if input('Пара чисел ' + str(couple) + ' считается \"удачной\". Изменить ее оценку? (Y) ') == 'Y':
						_ev = 0
					ev.append(_ev)
				
			if isWritable:
				writeToFile('data.txt', array, ev)
			isWritable = True
			if input('Продолжить? (Y) ') != 'Y':

				break

	else:
		print('Неизвестный аргумент запуска программы')
		print('Допустимые:')
		print('first - ввод пользователем массива и его оценки')
		print('second - автоматическая генерация массивов в указанном количестве и диапазоне и ввод пользователем их оценок')
		print('third - программа генерирует \"удачные\" пары чисел в заданном количестве, а пользователь может изменить оценку пары')