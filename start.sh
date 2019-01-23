./stop.sh

rm nohup.out
git pull origin master
nohup sudo python3 bot.py & 

