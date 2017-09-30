#!/bin/bash
echo Installing PIP requirements...
sudo pip install -r requirements.txt -U
echo Copying scripts...
sudo mkdir -p /usr/share/workspaces
sudo cp -fr workspaces/* workspaces.sh /usr/share/workspaces/
sudo cp workspaces.completion.sh /etc/bash_completion.d/
if [ ! -e "/etc/workspaces.yml" ]; then
    sudo cp workspaces.yml /etc/
fi
echo "To activate, open a new bash instance (executable name is 'workspaces')."
