brew doctor > /dev/null 2> /dev/null || \
    echo "Brew is not fine, please fix it" || \
    exit

brew_binaries=(
    ssh-copy-id
    brew-cask
    cairo
    cmake
    dtrx
    fontconfig
    freetype
    gdbm
    gettext
    glib
    go
    htop-osx
    irssi
    libffifd
    libpng
    mercurial
    mobile-shell
    openssl
    p7zip
    pcre
    pixman
    pkg-config
    protobuf
    rust
    tree
    unrar
    wget
    xz
    yasm
    zsh
)

brew_cask_app=(
    alfred
    dash # documentation offline
    sublime-text3
    xquartz
    lauch
    amethyst
    iterm2
    mactex
    macvim
    totalspaces
    virtualbox
)

brew install $brew_binaries
brew cask install $brew_cask_app
brew cask alfred

brew doctor

sh ./install_cargo.sh
