./stop.sh

rm nohup.out
git fetch
git reset --hard origin/master
nohup sudo python3 bot.py & 

