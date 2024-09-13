SOURCE="C:/Users/james/Box/Chung lab data/EVOS images/JP/SC/08.21/"

for dir in "$SOURCE"*/
do
    mkdir "$dir"channel
    find "$dir" -type f -name "*[A-z].tif" -exec mv -v {} "$dir"channel \;
done