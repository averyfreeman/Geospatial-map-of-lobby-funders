#!/bin/sh
cd /app
echo "creating animations"
python bar_chart.py
python geospatial_map.py
echo "your animations are built - check the recordings folder"
echo "if the animation files are not there for sone reason, you"
echo "can try downloading them from inside the container using"
echo "a self-hosted web server I set up."
echo "To use it, uncomment the last line of "
echo "docker-entrypoint.sh and re-build the container image" 
# echo "     http://$(hostname -i):8000"
# echo "If CTRL-C doesn't stop it, may have to run"
# echo "\`docker kill\` in another terminal"
# python -m http.server --bind $(hostname -i | cut -d ' ' -f1) --directory recordings