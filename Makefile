# Delete pycache, build, and zip files
clean:
	@rm -rf */__pycache__
	@rm -rf *.zip
	@rm -rf build/
	@rm -rf bin/

# Download chromedriver, headless-chrome to `./bin/`
fetch-dependencies:		
	@mkdir -p bin/

	# Get chromedriver
	@if [ ! -e chromedriver.zip ]; \
		then curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip; \
	fi;	
	unzip -o chromedriver.zip -d bin/

	# Get Headless-chrome
	@if [ ! -e headless-chromium.zip ]; \
		then curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip; \
		fi;
	unzip -o headless-chromium.zip -d bin/

	@rm -rf *.zip

# Prepare build.zip archive for AWS Lambda deploy 
build: clean fetch-dependencies
	mkdir build build/lib
	cp -r src/* build/.
	cp -r bin build/.
	cp -r lib build/.
	cp -r env/lib/python3.8/site-packages/*  build/.
	cd build; rm -rf __pycache__/ *.dist-info; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build
