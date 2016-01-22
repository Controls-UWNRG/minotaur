Minotaur
========
UWaterloo Nano Robotics Group Controls Software
------------------------------------------------------------

###Setup
####Linux/MacOS
First, make sure that you have `pip` installed. The installation structure varies from distro to distro.The required libraries to run the code are pyserial, numpy, and pygtk. We use python 2.x for all the code, so if you are on Linux, make sure to run the commands as `sudo pip2 install` and `python2 main.py` when installing packages and running the code, respectively.

####Windows
Refer to the [Third Party Software](https://github.com/Controls-UWNRG/minotaur/wiki/Third-Party-Libraries) page of the wiki for setting up the code on Windows. Using Git bash is highly recommended for using `git` commands.

####Cloning and running the code
Once you have downloaded all the required dependencies, go ahead and clone this repository:
```
git clone https://github.com/Controls-UWNRG/minotaur.git
```
Then navigate to the `UWNRG_CURRENT` folder (we really need a better name) and run `python main.py` (or `python2 main.py` if you have python 3.x installed). Make sure to include `--noport` as a flag when running the code on your personal machine so that the program ignores the absense of the actuator connection.

###Other questions
The [wiki](https://github.com/Controls-UWNRG/minotaur/wiki/) has a lot of resources in case you want more information. It's pretty ancient though.

###C++ Migration
####Goals and Requirements:
* Cross-platform development and deployment
* Maintainable object-oriented architecture
* Abstracted implementation and approachable interface
* High-speed architecture for real-time data crunching (read image recognition)
* More to come...
