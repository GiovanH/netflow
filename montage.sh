#!/bin/bash
#Seth Giovanetti
#Uses imagemagick to show graphs over time.

echo Working Magick

mkdir montage 2>/dev/null
rm -rv ./montage/*.png

for imagename in graph graph_regression_4
do
  echo $imagename
  for command in `ls ./out/prev20180110_+0.csv/`
  do
    echo $command
    magick="magick montage -label %d"
    for glob in ./out/*000.csv
    do
     magick="$magick ${glob}/${command}/${imagename}.png"
    done
    `$magick  -geometry 100% -tile 8x3 -gravity north -shadow montage/${command}_${imagename}_8x3.png`
    `$magick  -geometry 100% -gravity north -shadow montage/${command}_${imagename}_autosize.png`
  done
done
