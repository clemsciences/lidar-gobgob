# LIDAR for GOBGOB
Code of data treatment for the 2019 France robotics cup.

# Installation


|        Etapes         |                           Actions                              |
|:---------------------:|:--------------------------------------------------------------:|
|0                      |Use Python 3  and pip3 (python-pip3)                            |
|1                      |Clone the repository.                                           |
|2                      |sudo pip3 install -r requirements.txt                           |
|3                      |Install tk8.6 (sudo pacman -S tk or sudo apt-get install tk).   |
|4                      |Enjoy !                                                         |

# Choice of application
You can:
- either show the obstacles on the screen ("hl_connected = False" in config.ini)
- either connect with a java server that has launched the python main.py before ("hl_connected = True" in config.ini)

# Debug

If you're using PyCharm, you might have to desactivate the
scientific display mode in order to see our display.

# TODO
- [x] Detect and display obstacles
- [x] Kalman filter implementation
- [x] Sockets for communication with the Java high-level
- [x] Logging
- [ ] Solve "Cleaning buffer..." issue with rplidar
- [ ] Cleaner shutdown(Tk, thread, serial errors when stopping)
- [ ] Locate precisely the position of our robot
