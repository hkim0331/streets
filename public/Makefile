all: install

install:
	rsync -avc --exclude Makefile ./ ubuntu@streets.melt.kyutech.ac.jp:/srv/streets/public/

clean:
	${RM} *~ *.bak


