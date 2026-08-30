# pdflatex engine
$pdf_mode = 1;

# Intermediate build artifacts
$aux_dir = 'build';

# Final PDFs
$out_dir = 'dist';

# Add repo root to TeX search path so presentations/*.tex find preamble.tex
ensure_path('TEXINPUTS', './');
