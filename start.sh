./stop.sh

rm nohup.out
git reset --hard origin/master
nohup sudo python3 bot.py & 

