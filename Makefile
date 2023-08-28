.PHONY: build run-service

build:
	python3 src/main.py

run-service:
	uvicorn src.main:app --reload

