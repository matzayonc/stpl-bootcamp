PRES_DIR   = presentations
BUILD_DIR  = build
DIST_DIR   = dist

SOURCES := $(wildcard $(PRES_DIR)/*.tex)
PDFS    := $(patsubst $(PRES_DIR)/%.tex,$(DIST_DIR)/%.pdf,$(SOURCES))

# Decks that ship in a GitHub release: everything except 99_* (templates,
# scratch, one-off talks) and archive_* (retired material)
RELEASE_PDFS := $(filter-out $(DIST_DIR)/99_% $(DIST_DIR)/archive_%,$(PDFS))

# Default presentation for single-target commands (override with PRES=name)
PRES ?= $(basename $(notdir $(firstword $(SOURCES))))

.PHONY: all open clean pptx release

all: $(PDFS)

release: $(RELEASE_PDFS)

$(DIST_DIR)/%.pdf: $(PRES_DIR)/%.tex preamble.tex scripts/dedupe_overlays.py
	mkdir -p $(BUILD_DIR) $(DIST_DIR)
	latexmk $<
	python3 scripts/dedupe_overlays.py $@

open: $(DIST_DIR)/$(PRES).pdf
	xdg-open $<

# Convert to PPTX via LibreOffice (best Google Slides compatibility)
pptx: $(DIST_DIR)/$(PRES).pdf
	libreoffice --headless --infilter="impress_pdf_import" --convert-to pptx --outdir $(DIST_DIR) $<

clean:
	latexmk -C $(SOURCES)
	rm -rf $(BUILD_DIR) $(DIST_DIR)

# Build all presentations whose filename contains the given filter, e.g. make 2
# Also supports make pptx-2, make slides-2, make open-2, make convert-2
define filter_pdfs
$(shell ls $(PRES_DIR)/*$(1)*.tex 2>/dev/null | sed 's|$(PRES_DIR)/|$(DIST_DIR)/|g; s|\.tex|.pdf|g')
endef

%:
	@pdfs="$(call filter_pdfs,$@)"; \
	test -n "$$pdfs" || { echo "No presentations matching '$@'"; exit 1; }; \
	$(MAKE) $$pdfs

pptx-%:
	@pdfs="$(call filter_pdfs,$*)"; \
	test -n "$$pdfs" || { echo "No presentations matching '$*'"; exit 1; }; \
	for pdf in $$pdfs; do \
	  $(MAKE) $$pdf && \
	  libreoffice --headless --infilter="impress_pdf_import" --convert-to pptx --outdir $(DIST_DIR) $$pdf; \
	done

open-%:
	@pdfs="$(call filter_pdfs,$*)"; \
	test -n "$$pdfs" || { echo "No presentations matching '$*'"; exit 1; }; \
	for pdf in $$pdfs; do $(MAKE) $$pdf && xdg-open $$pdf; done
