target_size = 0
import os
for dirpath, dirs, files in os.walk('movie_image\\'):
    for file in files:
        path = os.path.join(dirpath, file)
        if os.stat(path).st_size == target_size:
            #print "haha"
            os.remove(path)