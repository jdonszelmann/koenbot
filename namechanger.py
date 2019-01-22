import random 


def generate_expr(a,b):

	infront = ""
	operator = "^"

	def invertandor():
		nonlocal operator,a,b,infront

		if random.choice([True,False]):
			if  a.startswith("¬") and operator == "v":
				a = a[1:]
				operator = "->"

			elif b.startswith("¬") and operator == "^" and infront.startswith("¬"):
				b = b[1:]
				operator = "->"
				infront = infront[1:]
			return

		if operator == "->":
			choice = random.choice([0,1,2,3,4,5,6])
			if choice == 1:
				operator = "v"
				a = "¬" + a
			elif choice == 2:
				operator = "^"
				b = "¬" + b
				infront = "¬" + infront

			elif choice == 3:
				if a.startswith("¬") and b.startswith("¬"):
					if random.choice([True,False]):
						a = a[1:]
						b = b[1:]
						a,b=b,a
					else:
						a = "¬" + a
						b = "¬" + b
						a,b=b,a
				else:
					a = "¬" + a
					b = "¬" + b
					a,b=b,a
			return

		choice = random.choice([0,1,2])

		if choice == 0:
			if a.startswith("¬") and b.startswith("¬") and infront.startswith("¬"):
				a = a[1:]
				b = b[1:]
				infront = infront[1:]
				if operator == "v":
					operator = "^"
				elif operator == "^":
					operator = "v"
			else:
				a = "¬" + a
				b = "¬" + b
				infront += "¬"
				if operator == "v":
					operator = "^"
				elif operator == "^":
					operator = "v"
		elif choice == 1:
			a = "¬" + a
			b = "¬" + b			
			infront += "¬"
			if operator == "v":
				operator = "^"
			elif operator == "^":
				operator = "v"

	while random.choice([True,True,True,True,True,True,True,True,True,False]):
		invertandor()

	while infront.startswith("¬¬¬¬¬"):
		infront = infront[2:]

	while a.startswith("¬¬¬¬¬"):
		a = a[2:]
	while b.startswith("¬¬¬¬¬"):
		b = b[2:]

	name = "(" + infront + "(" + a + " " + operator + " " + b + ")" + ")"
	return name