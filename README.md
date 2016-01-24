Minotaur
========
UWaterloo Nano Robotics Group Controls Software
------------------------------------------------------------

### Setup
#### Linux/MacOS
First, make sure that you have `pip` installed. The installation structure varies from distro to distro.The required libraries to run the code are pyserial, numpy, and pygtk. We use python 2.x for all the code, so if you are on Linux, make sure to run the commands as `sudo pip2 install` and `python2 main.py` when installing packages and running the code, respectively.

#### Windows
Refer to the [Third Party Software](https://github.com/Controls-UWNRG/minotaur/wiki/Third-Party-Libraries) page of the wiki for setting up the code on Windows. Using Git bash is highly recommended for using `git` commands.

#### Alternative (easier) setup on Windows: Cygwin
[Cygwin](https://cygwin.com/) is a great unix-style set of packages and terminal on Windows. When running the setup, you can choose any set of packages that you want, but in addition, you need the following packages:
* `python`
* `python-setuptools`
* `python-cv`
* `python-gtk`
* `git`
* `xorg-server`
* `xinit`
* `xlaunch`
* `xorg-docs` (optional, for man pages)

Once the installation is finished, you can launch the cygwin terminal and type `easy_install-2.x pip` where 2.x is the version of python that you have. If you are not sure about what version you have, run `python -V` (only include the first two digits, e.g. 2.7 if version is 2.7.10). You can then install all the python libraries using `pip install` using the same instructions as MacOS and Linux users.

You have to run the program from an X terminal, so run `xinit -multiwindow -clipboard` to launch an xterm. Run your code from the terminal that opens up.

#### Cloning and running the code
Once you have downloaded all the required dependencies, go ahead and clone this repository:
```
git clone https://github.com/Controls-UWNRG/minotaur.git
```
Then navigate to the `UWNRG_CURRENT` folder (we really need a better name) and run `python main.py` (or `python2 main.py` if you have python 3.x installed). Make sure to include `--noport` as a flag when running the code on your personal machine so that the program ignores the absence of the actuator connection.

### Other questions
The [wiki](https://github.com/Controls-UWNRG/minotaur/wiki/) has a lot of resources in case you want more information. It's pretty ancient though.

***

### C++ Migration
#### Why C++? Why the migration?
Python is situationally a great language. It feels intuitive when you're dealing with small programs. [It's all fresh in your head](http://qr.ae/Rgd6JH) since you are dealing with a minimal number of custom objects/types. However, as a project gets bigger, and extends to thousands of lines of code, it becomes extremely hard to look at a codebase that you are either unfamiliar with or haven't worked with in recent times. One of the main reasons for this is that Python is a [dynamically-typed language](https://en.wikipedia.org/wiki/Dynamic_programming_language). And also the fact that python has terrible object-oriented programming features is just more fuel to the fire. Let's not even talk about real-time performance of the language, that's a long rant.  

C++ is not an angel either. However, good structural foundations in a powerful object-oriented language would help all future collaborators when they contribute to and maintain the project, and C++ is one of the best out there. This is very important for the long term development cycle, for reasons discussed above. C++ has its fair share of downsides also, e.g. it is a very mature language which makes it difficult to understand for newer programmers unfamiliar with a lot of advanced programming concepts. Moreover, it might not feel as intuitive for people who never worked with real programming languages like C/C++ (*#rekt*). All jokes aside, for the dedicated contributors like **you**, these should not be that big of an issue :smile:. And also, the pros of using C++ over Python grandly outweighs the cons, even including all the effort required to rewrite the entire project. So here we are.

#### Goals and Requirements
* Cross-platform development and deployment
* Maintainable object-oriented architecture
* Abstracted implementation and approachable interface
* High-speed architecture for real-time data crunching (read image recognition)  

*More to come...*

#### Development
##### Setup
For now, you only need to get the [Qt Framework](http://www.qt.io/download/). You can also get Qt Creator in order to build the code with one button and use their form editor for easy GUI design. You can open the project by specifying the folder `minotaur` and then build and run the code from there.

##### Contributing
Any help would be greatly appreciated. The entire code base is pretty big, there is a lot of code to be rewritten. If you want to help out, let [me](https://github.com/sadmansk) and we will figure something out.
