current_path=`pwd`

echo $current_path
ln -sf $current_path/./zsh/zshrc ~/.zshrc
ln -sf $current_path/./irssi ~/.irssi
#ln -s $current_path/./i3 ~/.i3
ln -sf $current_path/./vim/vimrc.before.local ~/.vimrc.before.local
ln -sf $current_path/./vim/vimrc.local ~/.vimrc.local
ln -sf $current_path/./vim/ycm_extra_conf.py ~/.ycm_extra_conf.py