from distutils.core import setup, Extension
 
module = Extension('hashModule', sources = ['./src/Cypher.c', './src/Hash.c', './src/main.c'])
 
setup (name = 'hashElGamal',
        version = '1.0',
        description = 'This is a implementation of hash function',
        ext_modules = [module])
