# Made by vhb
triple=x86_64-apple-darwin
curl -O https://static.rust-lang.org/cargo-dist/cargo-nightly-$triple.tar.gz
tar xf cargo-nightly-$triple.tar.gz
sudo ./cargo-nightly-$triple/install.sh
rm -fr cargo-nightly-$triple.tar.gz cargo-nightly-$triple
