date=`date +%Y-%m-%d`
python get_new_movie.py ../conf/template ../data/movie.$date ../data/link.$date /home/wangwei/moviesite/moviesite/static/photos/pic/ |tee ../log/log.$date
cp ../data/movie.$date ../data/movie
cp ../data/link.$date ../data/link

cd /home/wangwei/moviesite/moviesite/
python db/update.py |tee update.log
