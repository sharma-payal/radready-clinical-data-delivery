.PHONY: demo test clean

demo:
	PYTHONPATH=src python3 -m radready demo

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

clean:
	PYTHONPATH=src python3 -m radready clean
