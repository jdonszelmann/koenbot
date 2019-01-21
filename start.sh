./stop.sh

rm nohup.out
git pull origin master
nohup python3 bot.py & 

