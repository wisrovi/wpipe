# Makefile for wpipe Documentation

TEXFILE = wpipe_documentation
PDFFILE = $(TEXFILE).pdf

.PHONY: all clean pdf view install-deps

all: pdf

pdf: $(PDFFILE)

$(PDFFILE): $(TEXFILE).tex sources/*.png sources/*.jpg
	@echo "Building $(PDFFILE)..."
	@pdflatex -interaction=nonstopmode $(TEXFILE).tex
	@pdflatex -interaction=nonstopmode $(TEXFILE).tex
	@pdflatex -interaction=nonstopmode $(TEXFILE).tex
	@echo "Done! Output: $(PDFFILE)"

view: $(PDFFILE)
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(PDFFILE); \
	elif command -v open > /dev/null; then \
		open $(PDFFILE); \
	else \
		echo "Open $(PDFFILE) manually"; \
	fi

clean:
	@rm -f $(PDFFILE)
	@rm -f $(TEXFILE).aux
	@rm -f $(TEXFILE).log
	@rm -f $(TEXFILE).out
	@rm -f $(TEXFILE).toc
	@rm -f $(TEXFILE).lot
	@rm -f $(TEXFILE).lof
	@rm -f $(TEXFILE).lol
	@rm -f $(TEXFILE).fls
	@rm -f $(TEXFILE).fdb_latexmk
	@rm -f $(TEXFILE).synctex.gz
	@echo "Cleaned!"

install-deps:
	@echo "Installing LaTeX dependencies..."
	@if command -v apt-get > /dev/null; then \
		sudo apt-get update && sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended; \
	elif command -v brew > /dev/null; then \
		brew install --cask mactex; \
	else \
		echo "Please install LaTeX manually from: https://www.latex-project.org/get/"; \
	fi

help:
	@echo "wpipe Documentation Build System"
	@echo ""
	@echo "Targets:"
	@echo "  make pdf           - Build PDF document"
	@echo "  make view          - Build and open PDF"
	@echo "  make clean         - Remove generated files"
	@echo "  make install-deps  - Install LaTeX dependencies"
	@echo "  make help          - Show this help"
