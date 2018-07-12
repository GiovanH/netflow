#!/bin/bash
#Seth Giovanetti
#Uses imagemagick to show graphs over time.

mkdir montage 2>/dev/null
rm -rv ./montage/*.png

for command in `ls ./out/prev20180110_+0.csv/`
do
  echo $command
  magick="magick montage -label %d"
  for glob in ./out/*000.csv
  do
    for image in `ls ${glob}/${command}/*.png`
    do
      # echo $image
      magick="$magick $image"
    done
  done
  magick="$magick  -geometry 100% montage/$command.png"
  echo $magick
  `$magick`
done
