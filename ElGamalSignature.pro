TEMPLATE = app
CONFIG += console
CONFIG -= qt

SOURCES += hash/src/Cypher.c \
    hash/src/Hash.c \
    hash/src/main.c \
    hash/src/test.c

HEADERS += \
    hash/src/Cypher.h \
    hash/src/Log.h \
    hash/src/Hash.h

