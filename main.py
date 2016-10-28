import sys
sys.path.append('signature')
import os
import re

from Signature import Signature
import hashModule
from optparse import OptionParser

class ACTION:
    calculation = 0
    check = 1
    debug = 2

parser = OptionParser()
parser.add_option("-d", "--data", dest="data", help="Path to a file with data")
parser.add_option("-r", "--report", dest="report", help="Path to a file with report")
parser.add_option("-a", "--action", dest="action", help="A action which will be executed (calc, check)")
parser.add_option("-p", "--path", dest="path", help="Path to file during check.")
(options, args) = parser.parse_args()

if options.data is None:
	print "File with data must be provided"
	exit()
if options.action == "calc":
	options.action = ACTION.calculation
elif options.action == "check":
	options.action = ACTION.check
elif options.action == "debug":
	options.action = ACTION.debug
else:
	print "Unrecognized action. (see help)"
	exit()

###############################################################################
class ElGamalSignatureIO(object):
	@staticmethod
	def writeElGamalSignature(sign, path_report, path_orig):
		with open(path_report, "w+") as f:
			f.write("{0}/{1}\n".format(os.getcwd(), path_orig))
			f.write("H = {0}\n".format(format(sign["H"], "016x")))
			f.write("Y = {0}\n".format(format(sign["Y"], "032x")))
			f.write("K = {0}\n".format(format(sign["K"], "032x")))
			f.write("S = {0}\n".format(format(sign["S"], "032x")))

	@staticmethod
	def readParseElGamalSignature(path_report):
		result = {}
		path = None
		text = None
		with open(path_report, "r") as f:
			path = f.readline()
			text = f.read()
		path = re.sub(r'\\', '/', path)
		result["path"] = re.sub('[^a-zA-Z0-9/.]', '', path)
		check_sig = re.compile(r"H\s*=\s*(?P<H>[0-9A-Fa-f]+)\s*Y\s*=\s*(?P<Y>[0-9A-Fa-f]+)\s*"
						"K\s*=\s*(?P<K>[0-9A-Fa-f]+)\s*S\s*=\s*(?P<S>[0-9A-Fa-f]+)",
					0).search(text).groupdict()

		result.update((key, int(value, 16)) for key, value in check_sig.items())
		return result

#############################################################################

def do_calculation(options):
	if options.report is None:
		options.report = "report.txt"
		print "Creating file for report ({0}/{1})".format(os.getcwd(), options.report)
	hash = hashModule.get_hash(options.data)
	sign = Signature.getSignature(hash)
	sign["H"] = hash	
	ElGamalSignatureIO.writeElGamalSignature(sign, options.report, options.data)
	print "\nSignature was successful write to {0}/{1}".format(os.getcwd(), options.report)

def do_check(options):
	readSign = ElGamalSignatureIO.readParseElGamalSignature(options.data)
	if os.path.isfile(readSign["path"]) is False:
		print "File does not exist '{0}'".format(readSign["path"])
		exit()
	if options.path is None:
		hash = hashModule.get_hash(readSign["path"])
	else:
		hash = hashModule.get_hash(options.path)
	sign = Signature.getSignature(hash)
	if readSign["H"] == hash and Signature.verificationSignature(readSign) is True:
		print "\nSignature is correct."
	else:
		print "\nSignature is incorrect."
		print "Read data"
		for x, y in readSign.items():
			if x != "path":
				print "\t{0} is {1}".format(x, format(y, "032x"))
		print "Caclulated signature"
		for x, y in sign.items():
			print "\t{0} is {1}".format(x, format(y, "032x"))

def do_debug(options):
	hash = hashModule.get_hash(options.data)
	Signature.debugVerificationSignature(hash)





if options.action == ACTION.calculation:
	do_calculation(options)
elif options.action == ACTION.check:
	do_check(options)
else:
	do_debug(options)
	