while true; do
    read -p "Do you wish autorun script?" yn
    case $yn in
        [Yy]* ) echo "Doing autorun script...";python3 /home/pi/CODEBARREraspi_program-master/CODEBARREraspi_program.py; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done