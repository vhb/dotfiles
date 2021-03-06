# Install scripts for CentOS
# This script is made to help me easaly setup a cent-os developpement evironnement

# Add EPEL repositories
EPEL_FILE=epel-release-7-5.noarch.rpm
wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/$EPEL_FILE
rpm -ivh epel-release-7-5.noarch.rpm
rm -fr $EPEL_FILE

# Install base stuffs
dnf install sudo
dnf groupinstall -y development # Way to much thing but way to easy

# Add some usefull stuff
dnf install -y zsh strace cmake htop mosh mlocate zlib-dev xz-libs openssl-devel sqlite-devel bzip2-devel 

# Setup docker
dnf -y install docker
chkconfig docker on
service docker start

# Setup python modules
dnf -y install python-pip 
pip install virtualenv

USERNAME=vhb

adduser $USERNAME
echo "$USERNAME ALL=(ALL) ALL" >> /etc/sudoers
chsh vhb -s /usr/bin/zsh

sudo updatedb
