sudo aptitude -y install git-core build-essential

mkdir -p $HOME/src && cd $HOME/src

#################
### FREEQUERY ###
#################
if [ -e $HOME/src/freequery ]
then
	cd $HOME/src/freequery && git pull origin master
else
	git clone 'git://github.com/sqs/freequery.git' $HOME/src/freequery && \
	cd $HOME/src/freequery
fi
sudo make install

#############
### DISCO ###
#############
if [ -e $HOME/src/disco ]
then
	cd $HOME/src/disco && git pull origin master
else
	git clone 'git://github.com/sqs/disco.git' $HOME/src/disco && \
	cd $HOME/src/disco
fi
make && sudo make install && cd contrib/discodex && sudo python setup.py install
