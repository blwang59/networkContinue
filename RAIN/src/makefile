CC=g++
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=Main.cpp Util.cpp Data.cpp Model.cpp Analyzer.cpp Test.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=main

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

