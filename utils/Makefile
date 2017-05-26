hcc:
	ruby hcc.rb > hcc.html

install-hcc: hcc
	mv hcc.html 1731* ../public

smnsk:
	ruby smnsk.rb > smnsk.html

install-smnsk: smnsk
	mv smnsk.html 15* 16* ../public

# kyutech:
# 	ruby kyutech.rb > kyutech.html

# intall-kyutech: kyutech
# mv kyutech.html 1710* 1610* ../public

clean:
	${RM} -rf 1731* hcc.html
	${RM} -rf 15* 16* smnsk.html
