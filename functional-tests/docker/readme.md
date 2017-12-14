Once the docker image is running:

* cd /home/chrome 
* git clone <https://github.com/rstens/BDDStack.git>
* cd BDDStack
* ./gradlew chromeHeadlessTest or 
* If you want to run ./gradlew firefoxHeadlessTest, first run:

Xvfb :1 -screen 0 1024x768x24 &

export DISPLAY=:1

