clean:
	rm -rf build build.zip
	rm -rf __pycache__

fetch-dependencies:
	# mkdir -p bin/
	# mkdir -p lib/

	# Get chromedriver
	curl -SL https://chromedriver.storage.googleapis.com/2.46/chromedriver_linux64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# Get Headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# Clean
	rm headless-chromium.zip chromedriver.zip

docker-build:
	# mkdir -p bin/
	# mkdir -p lib/
	docker-compose build

docker-run:
	docker-compose run lambda src/lambda_function.lambda_handler

build-lambda-package: clean
	mkdir build
	cp -r src build/.
	# cp -r bin build/.
	# cp -r lib build/.
	# pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build