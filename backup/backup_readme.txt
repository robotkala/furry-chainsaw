In order to turn dump.rdb to dump.json for human readable format do:

docker build -t dump-to-json .
docker run -d -v /<this folder FULL path>:/home dump-to-json

and enjoy your json !
