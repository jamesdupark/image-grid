BASE_DIRECTORY="C:/Users/james/Box/Chung lab data/EVOS images/JP/SC/08.21/"
NAME_STEM="5xFAD*"

find "$BASE_DIRECTORY" -type f -name "result.png" -delete ;
find "$BASE_DIRECTORY" \
-type d -maxdepth 1 -mindepth 1 \
-exec sh -c 'C:/Users/james/Projects/venv/cs1951_env/Scripts/python.exe c:/Users/james/Projects/playground/datavis/image_grid.py "{}/"' \;

# find "$BASE_DIRECTORY" \
# # executes on all directories starting with name_stem /// TODO: max/mindepth
# -type d -name $NAME_STEM \
# # executes only on all immediate subdirectories
# -type d -maxdepth 1 -mindepth 1 \
# -exec sh -c 'C:/Users/james/Projects/venv/cs1951_env/Scripts/python.exe c:/Users/james/Projects/playground/datavis/image_grid.py "{}/"' \;