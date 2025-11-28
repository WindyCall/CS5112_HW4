\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{hw}

\LoadClass[12pt]{article}
\RequirePackage[utf8]{inputenc}
\RequirePackage[margin=1in]{geometry}

\RequirePackage{libertine}
\RequirePackage{parskip}

\RequirePackage{amsthm,amsmath,amssymb,hyperref}
\RequirePackage{tikz}
\usetikzlibrary{arrows,automata}

\RequirePackage{pgfplots}
\pgfplotsset{compat=1.16}

\pagestyle{plain}
\thispagestyle{empty}

\definecolor{carnellian}{RGB}{190,20,20}

\usepackage{dirtree}
\usepackage{nimbusmononarrow}

\newcommand{\N}{\mathbb{N}}
\newcommand{\bigO}{\mathcal{O}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Problems:

\theoremstyle{definition}
\newtheorem{problem}{Problem}

\newcounter{subq}[problem]
\newenvironment{subproblem}
{\refstepcounter{subq} \begin{itemize} \item[(\alph{subq})]}
{\end{itemize} \medskip}

\setlength\fboxrule{.5mm}\setlength{\fboxsep}{1.2mm}
\newlength\courseheader
\setlength\courseheader\textwidth
\addtolength\courseheader{-4mm}

\AtBeginDocument{
    \fbox{
        \parbox{\courseheader}{
        CS 5112 Fall 2025\hfill HW\hwnum: {\it \title}  \\
        Name: \name \hfill \textbf{Due: \duedate}\\
        NetID: \netid \\
        Collaborators: \collaborators
        }
    }
    \vspace{5pt}
}

\RequirePackage{environ}
\NewEnviron{solution}[1][80pt]{
    \vspace{10pt} \textcolor{blue}{Answer: \BODY} \vspace{10pt}
}

% Challenge:
\newcommand{\challenge}{    
    \newpage

    \fbox{
        \parbox{\courseheader}{
        CS 5112 Fall 2025\hfill HW\hwnum: Challenge Problem  \\
        Name: \name \hfill \textbf{Due: \duedate}\\
        NetID: \netid \\
        Collaborators: \collaborators
        }
    }
    \vspace{5pt}

}