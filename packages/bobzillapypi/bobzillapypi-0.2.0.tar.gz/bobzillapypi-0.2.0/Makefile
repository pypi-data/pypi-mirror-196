all: install run

install: venv
	: # Activate venv
	. .env/bin/activate && pip install -r requirements.txt

venv:
	: # Create venv if it doesn't exist
	test -d venv || python3 -m venv .env

develop: install
	. .env/bin/activate && maturin develop

build: install
	. .env/bin/activate && maturin build

run: develop
	. .env/bin/activate && ./examples/ngrok-http-minimal.py

fullrun: develop
	. .env/bin/activate && ./examples/ngrok-http-full.py

runflask:
	. .env/bin/activate && python ./examples/flask-test.py

# e.g.: make test=TestNgrok.test_gzip_tunnel test
test: develop
	. .env/bin/activate && python ./test/test.py $(test)

# e.g.: make test=TestNgrok.test_gzip_tunnel testonly
testonly:
	. .env/bin/activate && python ./test/test.py $(test)

testpublish:
	. .env/bin/activate && maturin publish --repository testpypi


clean:
	rm -rf .env target/
