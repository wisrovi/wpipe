# Documentation Examples

## Example 1: Sphinx conf.py

```python
# examples/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'My Project'
copyright = '2024, wisrovi'
author = 'wisrovi'
version = '1.0'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
```

## Example 2: LaTeX Preamble

```latex
% examples/preamble.tex
\documentclass[12pt,a4paper]{report}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\usepackage{courier}
\usepackage{graphicx}
\usepackage{hyperref}

\geometry{
    left=2.5cm,
    right=2.5cm,
    top=2.5cm,
    bottom=2.5cm
}

\titleformat{\chapter}[display]
    {\normalfont\huge\bfseries\sffamily\color{blue!70!black}}
    {\chaptertitlename\ \thechapter}{20pt}{\Huge}
```

## Example 3: index.rst

```rst
examples/index.rst
============

Project Overview

.. image:: diagrams/system-architecture.png
   :alt: System Architecture
   :align: center

Contents:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api/modules
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

About the Author
================

**wisrovi**
AI Solutions Architect
```

## Example 4: Technical Whitepaper Chapter

```latex
\chapter{Architecture}
\cleardoublepage

\section{System Overview}

The system follows a microservices architecture with the following components:

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{sources/system-architecture.png}
    \caption{System Architecture - High-level overview}
    \label{fig:arch}
\end{figure}

\textit{Figure \ref{fig:arch} shows the primary system components.}

\section{Data Flow}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{sources/data-flow.png}
    \caption{Data Flow Diagram}
    \label{fig:flow}
\end{figure}

\section{Risk Matrix}

\begin{table}[htbp]
\centering
\caption{Technical Risk Assessment}
\begin{tabular}{|l|c|c|c|p{3cm}|}
\hline
Component & Risk & Prob & Impact & Mitigation \\
\hline
Database & High & 3 & 5 & Connection pooling \\
\hline
API Gateway & Medium & 2 & 4 & Rate limiting \\
\hline
\end{tabular}
\end{table}
```
