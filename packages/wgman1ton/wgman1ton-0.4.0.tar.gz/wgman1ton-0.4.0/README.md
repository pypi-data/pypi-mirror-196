# 1toN-wireguard-manager

Simple cli-tool to create the wg0.conf-files for a 1-to-many network infrastructure in which the N-peers can connect to each other via the 1-peer.

Note that the keys are stored in an unencrypted sqlite-file and the configs get exported as plain text files – use this on your own risk!

# installation

    pip install wgman1ton

You also need wireguard installed (the package is called `wireguard-tools` in many distributions).

# usage

    $ wgman1ton
    :: Select an option 
       1 edit general settings
       2 add node
       3 remove node
       4 display qr-code for node
       5 export all configs
       6 exit
    > █

Optionally you can also provide the name of the `.db`-file that should be opened.

    $ wgman1ton different.db

The software will create a database file called `wgman1ton.db` in the current directory to persist the configuration.

Navigate through the cli-menu. In the end export the configuration and distribute it to the appropriate peers.

Call the software from the same directory later to continue where you left off.
