FROM python:3.12.4-slim-bookworm
COPY --chmod=755 entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]