SOURCES = Makefile rama-project.tex vector-functions.py
TEXNAME=rama-project

all: latex
q: $(TEXNAME).tex $(SOURCES)
	xelatex -shell-escape $(TEXNAME)
latex: $(TEXNAME).pdf
$(TEXNAME).pdf: $(TEXNAME).tex $(SOURCES)
	xelatex -shell-escape $(TEXNAME)
	xelatex -shell-escape $(TEXNAME)
	xelatex -shell-escape $(TEXNAME)
smallclean:
	rm -f $(TEXNAME).blg $(TEXNAME).bbl $(TEXNAME).aux $(TEXNAME).log $(TEXNAME).nav
clean:
	rm -f *.o \#* *~ nn $(TEXNAME).aux $(TEXNAME).log $(TEXNAME).out *.pyg *.toc $(TEXNAME).bbl $(TEXNAME).blg $(TEXNAME).nav $(TEXNAME).snm $(TEXNAME)-blx.bib $(TEXNAME).run.xml $(TEXNAME).vrb missfont.log
diff:
	git-latexdiff --main $(TEXNAME).tex -o diff.pdf -v $(OLD)
rtf:
	xelatex -shell-escape $(TEXNAME)
	xelatex -shell-escape $(TEXNAME)
	xelatex -shell-escape $(TEXNAME)
	latex2rtf $(TEXNAME).tex

