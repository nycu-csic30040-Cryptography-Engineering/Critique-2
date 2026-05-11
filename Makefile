GROUP    := 01
CRITIQUE := $(GROUP)_critique.pdf
REPORT   := $(GROUP)_report.pdf
ZIP_DIR  := $(GROUP)_project2
ZIP_FILE := $(ZIP_DIR).zip
TYPST    := docker run --rm -v "$(CURDIR):/work" ghcr.io/typst/typst:0.14.2

.PHONY: typst pdf report zip clean

typst pdf: $(CRITIQUE)

$(CRITIQUE): critique.typ
	$(TYPST) compile /work/critique.typ /work/$(CRITIQUE)

report: $(REPORT)

$(REPORT): 01_report.typ
	$(TYPST) compile /work/01_report.typ /work/$(REPORT)

zip: $(CRITIQUE) $(REPORT)
	rm -rf "$(ZIP_DIR)" "$(ZIP_FILE)"
	mkdir -p "$(ZIP_DIR)"
	cp task1.py task2.py task3.py task4.py "$(ZIP_DIR)/"
	cp "$(CRITIQUE)" "$(ZIP_DIR)/$(CRITIQUE)"
	cp "$(REPORT)" "$(ZIP_DIR)/$(REPORT)"
	zip -r "$(ZIP_FILE)" "$(ZIP_DIR)"
	rm -rf "$(ZIP_DIR)"
	@echo "Created $(ZIP_FILE)"

clean:
	rm -f "$(CRITIQUE)" "$(REPORT)"
	rm -rf "$(ZIP_DIR)" "$(ZIP_FILE)"
