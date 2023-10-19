# 生成結果
RESULT=Koala-manygen/result
PLOT_RESULT=Koala-manygen/plot_result

all: build

.PHONY: all build clean
build:
	cd Koala-manygen && \
	javac -cp ../test/share/py4j/py4j0.10.9.5.jar:../java_class/:../PersistentHomologyOnGraphs-master/PHFDL0D/libusf/src/ -d ../java_class/ src/ocha/itolab/koala/**/*.java ../PersistentHomologyOnGraphs-master/PHFDL0D/libusf/src/usf/dvl/graph/**/*.java

run:
	cd Koala-manygen && \
	python3 ../java_class/ocha/itolab/koala/batch/py4j/main.py

clean:
	find ${RESULT} ${PLOT_RESULT} -type f -delete