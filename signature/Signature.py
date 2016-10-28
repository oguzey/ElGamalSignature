import re
import os

class Signature(object):
	p = int("AF5228967057FE1CB84B92511BE89A47", 16)
	a = int("9E93A4096E5416CED0242228014B67B5", 16)
	q = int("57A9144B382BFF0E5C25C9288DF44D23", 16)

	@staticmethod
	def hash2Number(hash):
		if isinstance(hash, int) or isinstance(hash, long):
			H = format(hash, "016x") + "00ffffffffffff00"
		elif isinstance(hash, str):
			H = hash + "00ffffffffffff00"
		else:
			raise Exception("Not supported hash type")
		H = re.findall('..', H)
		H = "".join(reversed(H))
		return int(H, 16)

	@staticmethod
	def __calculateSignature(hash):
		H = Signature.hash2Number(hash)
		a, q, p = Signature.a, Signature.q, Signature.p

		x = int(os.urandom(16).encode('hex'), 16)
		x = x % (p + 1)
		y = pow(a, x, p)

		U = int(os.urandom(16).encode('hex'), 16)

		Z = pow(a, U, p)

		Z_sh = (Z * H ) % p
		g = (x * Z * pow(Z_sh, q-2, q) ) % q

		k = (U - g) % q

		S = pow(a, g, p)

		print "\nCaclulation hash ..."
		print "#" * 40
		print "p is {0}".format(format(p, "032x"))
		print "a is {0}".format(format(a, "032x"))
		print "q is {0}".format(format(q, "032x"))
		print "x is {0}".format(format(x, "032x"))
		print "y is {0}".format(format(y, "032x"))
		print "H is {0}".format(format(H, "032x"))
		print "U is {0}".format(format(U, "032x"))
		print "Z is {0}".format(format(Z, "032x"))
		print "g is {0}".format(format(g, "032x"))
		print "k is {0}".format(format(k, "032x"))
		print "S is {0}".format(format(S, "032x"))
		print "#" * 40

		return {"H" : H, 
				"K": k, 
				"S": S, 
				"Y": y,
				"hash": hash,
				"x": x,
				"g": g}

	@staticmethod
	def getSignature(hash):
		sign = Signature.__calculateSignature(hash)
		return {"Y": sign["Y"],
				"K": sign["K"],
				"S": sign["S"]}

	@staticmethod
	def verificationSignature(data):
		a, q, p = Signature.a, Signature.q, Signature.p
		H = Signature.hash2Number(data["H"])
		print "\nVerification signature..."
		print "#" * 40
		common = (data["S"] * pow(a, data["K"], p)) % p

		left = pow(data["S"], (H * common) % p, p)
		print "left is  {0}".format(format(left, "032x"))

		right = pow(data["Y"], common, p)
		print "right is {0}".format(format(right, "032x"))
		return left == right
		
	@staticmethod
	def debugVerificationSignature(hash):
		data = Signature.__calculateSignature(hash)
		print "\nDEBUG-Verification to correct calculation..."
		print "#" * 40
		a, q, p = Signature.a, Signature.q, Signature.p
		x = data["x"]
		H = data["H"]
		g = data["g"]
		k = data["K"]
		st_l = g * ((H * pow(a, g + k, p)) % p)
		st_r = x * pow(a, g + k, p)

		l = pow(a, st_l, p)
		r = pow(a, st_r, p)

		l2 = g * H
		r2 = x
		print "l is {0}".format(format(l, "032x"))
		print "r is {0}".format(format(r, "032x"))
		print "l2 is {0}".format(format(st_l , "032x"))
		print "r2 is {0}".format(format(st_r , "032x"))
		print "ch1 is {0}".format(format(l2 / r2 , "032x"))
		print "ch2 is {0}".format(format(l2 % r2 , "032x"))
		print "#" * 40
