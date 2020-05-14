#!/bin/bash
set -e 


install_bmp () {
    bmp_url='https://api.github.com/repos/lightbody/browsermob-proxy/releases/latest'
    bmp_latest=$(curl --silent $bmp_url|grep '"tag_name":'|sed  --regexp-extended 's/.*"([^"]+)".*/\1/')

    if [ ${#bmp_latest} -eq 0 ]
    then
        echo "Can not find the latest Browsermob-proxy version"
        echo "continue installation without browsermob-proxy"
        return 1
    fi
    echo "latest tag is: $bmp_latest"
    local new_url=$(curl --silent $bmp_url | grep '"browser_download_url":'|sed  --regexp-extended 's/.*"([^"]+)".*/\1/')
    echo $new_url
    local dl_name=bmp_$RANDOM'.zip'
    curl -L  $new_url > $dl_name
    unzip -o $dl_name
    rm $dl_name
    mv $bmp_latest /home/screenshot/browsermob_proxy
}

apt-get update
apt-get install -y -f wget
apt-get install -y -f curl
apt-get install -y -f unzip
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
apt-get update -y
chrome_file='google-chrome-stable_current_amd64.deb'
wget -q -O $chrome_file 'https://dl.google.com/linux/direct/'"$chrome_file"
apt-get install -y -f ./"$chrome_file"
chrome_version=$(google-chrome --version | grep -E '[.0-9]{1,}' --only-matching)
if [ $? -ne 0 ]
then
    echo "Can not install the latest Google Chrome..."
    exit -1
fi
echo $chrome_version
dot_count=$(echo $chrome_version | sed -n --regexp-extended 's/[0-9]//gp')

if [ ${#dot_count} -ne 3 ] || [ $dot_count != '...'  ]
then
    echo "Can not extract the correct Chrome version"
    exit -1
fi
major_version=$(echo $chrome_version | sed -n --regexp-extended 's/([0-9]{1,}\.[0-9]{1,}\.[0-9]{1,})\.[0-9]{1,}/\1/p')
get_latest_url='https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'
driver_version=$(curl $get_latest_url$major_version)
echo $driver_version
tmp=$(echo $driver_version | grep -E '^([0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,})$')
if  [ $? -ne 0 ] || [ ${#tmp} -eq 0 ]
then
    echo "Can not get the latest chromedriver"
    exit -1
fi
new_url='https://chromedriver.storage.googleapis.com/'$tmp'/chromedriver_linux64.zip'
dl_name=chromedriver_$RANDOM'.zip'
echo "Downloading...$new_url"
curl  --silent $new_url > $dl_name
res1=$?
unzip -o $dl_name
res2=$?
if [ $res1 -ne 0 ] || [ $res2 -ne 0 ]
then
    echo "Can not download and/or extract zip file"
    exit -1
fi
rm -f $dl_name
cp chromedriver /bin/
apt-get install -f -y  python3
apt-get install -f -y  python3-pip
pip3 install cherrypy
pip3 install selenium
pip3 install tldextract
pip3 install pillow
echo "echo 'server is running...' " >> /home/screenshot/.bashrc
# not installing bmp anymore
#install_bmp
# remove java installation (not using bmp anymore)
#apt-get install -y -f default-jre
#chown --recursive screenshot:screenshot /home/screenshot/browsermob_proxy
#echo 'cd /home/screenshot/browsermob_proxy && nohup ./bin/browsermob-proxy -port 8046 &' >> /home/screenshot/.bashrc
echo 'cd /home/screenshot/ && python3 sc_api.py ' >> /home/screenshot/.bashrc
echo "Done!!!!!"
echo '***********************************'
echo '***********************************'
echo '***********************************'
echo '***********************************'
echo 'Now run the image using the following command.'
echo 'docker container run --rm -it  -p 8000:8086 --user screenshot <image-name>'
echo 'image-name: name of the image you just built'
echo 'Access to API using http://localhost:8000'
echo '***********************************'
echo '***********************************'
echo '***********************************'
echo '***********************************'
