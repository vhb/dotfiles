# Made by vhb
echo "This command disable login with password, please make sure that you do have set your authorized_key"
# Disable login with password
SSH_FILE=/etc/ssh/sshd_config
sed -i 's/^RSAAuthentication .*$/RSAAuthentication yes/' $SSH_FILE
sed -i 's/^PubkeyAuthentication .*$/PubkeyAuthentication yes/' $SSH_FILE
sed -i 's/^#RSAAuthentication .*$/RSAAuthentication yes/' $SSH_FILE
sed -i 's/^#PubkeyAuthentication .*$/PubkeyAuthentication yes/' $SSH_FILE
sed -i 's/^ChallengeResponseAuthentication .*$/ChallengeResponseAuthentication no/' $SSH_FILE
sed -i 's/^PasswordAuthentication .*$/PasswordAuthentication no/' $SSH_FILE
sed -i 's/^UsePAM .*$/UsePAM no/' $SSH_FILE
/etc/init.d/ssh reload

