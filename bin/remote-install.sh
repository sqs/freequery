# TODO(sqs): add disco user

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
make install

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
make && make install && cd contrib/discodex && python setup.py install

#############
### PATHS ###
#############
cp -R $HOME/src/disco/contrib/discodex/ /usr/local/lib/disco/
chown -R disco:disco /usr/local/lib/
mkdir -p /srv/disco /srv/disco/log /srv/disco/run /srv/disco/.ssh
chown -R disco:disco /srv/disco