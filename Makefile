all:
	cd metatranscirptome_uniform_de_novo && $(MAKE)
	rm -fv *pyc

.PHONY: all