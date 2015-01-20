# yum install core-utils gcc python git clang vim i3 i3lock dmenu dunst valgrind gdb golang
# echo 'exec i3' > ~/xinitrc
wget --no-check-certificate http://install.ohmyz.sh -O - | sh
curl https://j.mp/spf13-vim3 -L -o - | sh
git clone https://github/vhb/dotfiles.git
sh setup.sh
