# wpipe Documentation - LaTeX Build System

## Requirements

Install a LaTeX distribution:

### Ubuntu/Debian
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### macOS
```bash
brew install --cask mactex
```

### Windows
Install MiKTeX from https://miktex.org/

## Building the Document

### Quick Build

```bash
make
```

### Manual Build

```bash
# Compile three times for references
pdflatex wpipe_documentation.tex
pdflatex wpipe_documentation.tex
pdflatex wpipe_documentation.tex
```

### Using Makefile

```bash
# Clean previous builds
make clean

# Build PDF
make pdf

# View PDF
make view
```

## Output

The compiled document will be saved as:
- `wpipe_documentation.pdf`

## Troubleshooting

### Missing Fonts
```bash
sudo apt-get install texlive-fonts-extra
```

### Missing Packages
```bash
sudo apt-get install texlive-latex-extra
```

### Permission Issues
```bash
chmod +x build.sh
./build.sh
```

## Document Structure

```
docs_pdf/
├── sources/              # Images and assets
│   └── architecture.png
├── wpipe_documentation.tex  # Main LaTeX source
├── Makefile              # Build automation
├── README.md             # This file
└── wpipe_documentation.pdf   # Output (after build)
```
