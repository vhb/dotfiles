# Path to your oh-my-fish.
set -g OMF_PATH /Users/vhb/.local/share/omf

# Path to your oh-my-fish configuration.
set -g OMF_CONFIG /Users/vhb/.config/omf
set -gx PATH $PATH ~/.bin

function fish_user_key_bindings
    bind \cl 'clear; commandline -f repaint'
    bind \cc 'commandline "ctrl+c pressed"'
    echo "foo"
end


### Configuration required to load oh-my-fish ###
# Note: Only add configurations that are required to be set before oh-my-fish is loaded.
# For common configurations, we advise you to add them to your $OMF_CONFIG/init.fish file or
# to create a custom plugin instead.

# Load oh-my-fish configuration.
source $OMF_PATH/init.fish
