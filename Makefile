.PHONY: demo audit test clean

demo:
	PYTHONPATH=src python3 -m radready demo

audit:
	PYTHONPATH=src python3 -m radready audit

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

clean:
	PYTHONPATH=src python3 -m radready clean
