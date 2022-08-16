#!/bin/bash

case $1 in
"--build" | "-b" )
  docker-compose -f docker-compose.yml up --build
  ;;

"--delete" | "-d" )
  docker-compose -f docker-compose.yml down --rmi local
  ;;

"--test" | "-t" )
  export DOCKER_CMD="pytest"
  docker-compose -f docker-compose.yml up --build
  docker-compose -f docker-compose.yml down --rmi local
  ;;
esac
