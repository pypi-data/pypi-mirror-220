.PHONY: dev dev-watch publish publish-test build reinstall-test clean

dev:
	sudo python3 -m pip install --user -e .

dev-watch:
	while true ; do sudo python3 -m pip install --user -e . ; sleep 1 ; done

publish-test: build
	python3 -m twine upload --repository testpypi --skip-existing dist/*

publish: build
	python3 -m twine upload --skip-existing dist/*

build:
	python3 -m build

reinstall-test:
	pip uninstall pycompall -y && pip install -i https://test.pypi.org/simple/ pycompall

reinstall:
	pip uninstall pycompall -y && pip install pycompall

clean:
	rm -f dist/*