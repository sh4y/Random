from random import choice
import string

def main():
	text = raw_input("Enter your text: ")
	tarr = [character for character in text]
	rand = []
	for i in range(0, len(tarr)):
		rand.append(choice(string.ascii_letters))
	iterations = 0
	while rand != tarr:
		iterations += 1
		for ch in range(0, len(tarr)):
			if tarr[ch] == ' ':
				rand[ch] = ' '
			elif tarr[ch] != rand[ch]:
				rand[ch] = choice(string.ascii_letters)
		print(''.join(rand))
	print("Iterations taken: ", iterations)

main()

