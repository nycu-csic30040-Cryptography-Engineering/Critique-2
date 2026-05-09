.PHONY: typst pdf clean

typst pdf:
	docker run --rm -v "$(CURDIR):/work" ghcr.io/typst/typst:0.14.2 compile /work/critique.typ /work/critique.pdf

clean:
	rm -f "critique.pdf"
