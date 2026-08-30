# LaTeX beamer build environment for dynaprez.
# The official TeX Live image ships a full distribution, including
# latexmk, beamer and texlive-fontsextra (which provides the Archivo font).
FROM docker.io/texlive/texlive:latest

# LibreOffice (Impress + Draw for the PDF import filter) is needed for the
# `make pptx` PDF -> PPTX conversion.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libreoffice-impress libreoffice-draw \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY . /work

# LibreOffice needs a writable HOME for its profile.
ENV HOME=/tmp

# `make` is the entrypoint, so `docker run` takes the same args as `make`:
#
#   docker run --rm -v "$PWD/dist:/work/dist" <image>            # make (all)
#   docker run --rm -v "$PWD/dist:/work/dist" <image> 2          # make 2
#   docker run --rm -v "$PWD/dist:/work/dist" <image> pptx-2     # make pptx-2
#   docker run --rm -v "$PWD/dist:/work/dist" <image> PRES=1_intro pptx
#
# Mount a volume on /work/dist to get the built PDFs/PPTX back on the host.
ENTRYPOINT ["make"]
CMD ["all"]
