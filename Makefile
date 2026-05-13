GROUP    := 01
CRITIQUE := $(GROUP)_critique.pdf
REPORT   := $(GROUP)_report.pdf
ZIP_FILE := $(GROUP)_project2.zip
TYPST    := docker run --rm -v "$(CURDIR):/work" ghcr.io/typst/typst:0.14.2

.PHONY: typst pdf report zip clean

typst pdf: $(CRITIQUE)

$(CRITIQUE): critique.typ
	$(TYPST) compile /work/critique.typ /work/$(CRITIQUE)

report: $(REPORT)

$(REPORT): 01_report.typ
	$(TYPST) compile /work/01_report.typ /work/$(REPORT)

zip: $(CRITIQUE) $(REPORT)
	rm -f "$(ZIP_FILE)"
	zip -j "$(ZIP_FILE)" task1.py task2.py task3.py task4.py "$(CRITIQUE)" "$(REPORT)"
	@echo "Created $(ZIP_FILE)"

clean:
	rm -f "$(CRITIQUE)" "$(REPORT)" "$(ZIP_FILE)"
