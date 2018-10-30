.. _Installation:

Installation
============

Python environment
------------------

The following steps to set up a working environment are applicable for both, 
the Raspberry Pi or a laptop/computer. 
Remember, the modules can be used on a laptop/computer for remote controlling 
the Raspberry Pis GPIOs or on the Raspberry Pi itself, without any modifications
to be made in the source code.

Getting files
^^^^^^^^^^^^^

First step is creating a folder named ``360pibot`` in the Raspberry Pis ``home`` folder

.. code-block:: console

    cd ~
    mkdir 360pibot

and then connect the Raspberry Pi to the internet, open the projects github page, 
download the repository as a .zip file and unzip it in the created ``360pibot`` 
folder.

Another option is to clone the git repository to the ``home`` folder directly. 
This will automatically create the folder and download the project files. First, git 
will be installed if not already existing, then the repository will be cloned.

.. code-block:: console

    sudo apt-get update
    sudo apt-get install git
    cd ~
    git clone https://github.com/choeffer/360pibot

Both methods for getting the project files are also working on a laptop/computer.

Installing needed modules
^^^^^^^^^^^^^^^^^^^^^^^^^

Next step is to install the needed modules. They can be installed in the global 
Python 3 environment or in a virtual environment. The latter has the advantage 
that the packages are isolated from other projects (and also from the system wide 
installed/global once) and if things get messed up, the virtual environment can just 
be deleted and created from scratch again. For more information about virtual 
environments in Python, see venv1_ and venv2_ . First, installing with a 
virtual environment will be explainend, afterwards with using the global 
Python 3 environment.

With a virtual environment
""""""""""""""""""""""""""

On a Raspberry Pi first ensure that the packages ``python3-venv`` and ``python3-pip`` 
are installed. This has also to be checked on a Debian based distribution like 
Ubuntu/Mint. 

.. code-block:: console

    sudo apt-get update
    sudo apt-get install python3-venv python3-pip

Afterwards, navigate to the created ``360pibot`` folder and create a virtual 
environment named ``venv`` and activate it in the running terminal. 

.. note::

    The created ``venv`` folder is added in the .gitignore file and will therefore 
    not be tracked by git.

.. code-block:: console

    cd ~
    cd 360pibot
    python3 -m venv venv
    source venv/bin/activate

With the activated virtual environment (indicated by a ``(venv)`` in the beginning 
of the terminal prompt) now install the needed ``pigpio`` module.

.. code-block:: console

    pip3 install pigpio

Deactivating the running virtual environment can be done later by just typing 
``deactivate`` in the running terminal.

.. code-block:: console

    deactivate

.. note::

    For later using the installed module the virtual environment has to be activated 
    every time, because the pigpio package is installed inside it and not callable 
    from outside.

Without a virtual environment
"""""""""""""""""""""""""""""

In this case, just the following steps are needed. Then, the ``pigpio`` module will 
be installed in the global Python 3 environment.

.. code-block:: console

    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install pigpio


Installing modules for the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The whole documentation is done with Sphinx_ and can be extended or 
modified as needed for e.g. documenting own projects based on this or if 
extending functionality of the modules and documenting this. The standard docstring format 
(ReStructuredText_ (reST)) is used. The used theme is from `Read the Docs`_ 
where also the documentation is hosted. Therefore, two more modules are needed 
for beeing able to modify or extend the documentation. How to use Sphinx is not 
part of this documentation. But there are good introductions and tutorials 
which provide a good starting point, see docs1_ , docs2_ , docs3_ and docs4_ .

.. note::

    For the creation of the docs ``conf.py`` , ``index.rst`` , and folder structure etc. 
    the ``sphinx-quickstart`` command was used.

.. note::

    The created ``docs/build`` folder is added in the .gitignore file and will therefore 
    not be tracked by git. This folder contains the output after building the docs.

If using a venv

.. code-block:: console

    cd ~
    cd 360pibot
    python3 -m venv venv
    source venv/bin/activate
    pip3 install sphinx sphinx_rtd_theme

or if installing in the global Python 3 environment.

.. code-block:: console

    pip3 install sphinx sphinx_rtd_theme

There is also a ``requirements.txt`` available in the repository which 
will install the used versions of the modules which are used while 
experimenting/developing with the demo implementation and writing the 
documentation.

This can be done by using a venv

.. code-block:: console

    cd ~
    cd 360pibot
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

or by installing them in the global Python 3 environment.

.. code-block:: console

    pip3 install -r requirements.txt

The ``requirements.txt`` is created with ``pip3 freeze > requirements.txt``.

Raspberry Pi
------------

The following steps are specific to the Raspberry Pi. It is needed to install the 
``pigpio`` package, automate/enable starting the daemon at boot and then doing a reboot 
to activate the pigpio daemon. For more information see `pigpio_download`_  and remote_pin_ . 
For the demo implementation the package from the Raspbian repository is chosen, 
because then it is more guarenteed that it is good integrated in the system, even 
if the packages might be a bit older.

.. code-block:: console

    sudo apt-get update
    sudo apt-get install pigpio
    sudo systemctl enable pigpiod
    sudo reboot

.. note::

    If the Raspberry Pi is not responding anymore, it might help to restart the
    pigpio daemon on the Raspberry Pi. For that, SSH into the Raspberry Pi if 
    remotely working with it, otherwise use the local terminal, and execute the 
    following two commands.

    .. code-block:: console

        sudo systemctl daemon-reload
        sudo systemctl restart pigpiod.service

Hotspot and Remote access
^^^^^^^^^^^^^^^^^^^^^^^^^

Another step which improves programming the Raspberry Pi is to enable a hotspot on it, 
see pi_hotspot_ , so that the Raspberry Pi can be accessed remotely. This is recommended 
before proceeding using it. This will not be covered here because the offical documentation 
is good and is updated regularly to match the latest Raspbian changes.

Also make yourself familiar with using VNC_ or using remote_pin_ . Latter will again 
drastically improve the use of the modules, because e.g. IDEs can be used, the robot can 
freely move around and so on. The latter option will be shortly explained here.

So after enabling the hotspot feature on the Raspberry Pi and beeing connected with your 
laptop/computer to it, the follwing steps are needed to remote control the 
Raspberry Pis GPIOs. For a more detailed description see remote_pin_ .

First, in the Raspberry Pi configuration *Remote GPIO* has to be enabled. This can 
be done via GUI or ``sudo raspi-config``. This will allow remote connections while 
the pigpio daemon is running.

Then the environment variable has to be set while or before launching Python 3 or an IDE. 
This variable will point to the IP address (and optional port) on which the Raspberry Pi 
is accessable, on its own provided hotspot/network or on a WLAN it is connected to. 
There are also other possibilities available for configuring remote access. They are 
mentioned in the pgpio documentation, see pigpio_pi_ . E.g. the IP address and port 
can be passed as arguments if initializing a pigpio.pi() object.

.. code-block:: console

    PIGPIO_ADDR=192.168.1.3 python3 hello.py
    PIGPIO_ADDR=192.168.1.3 python3 code .

References
----------

.. target-notes::

.. _venv1: https://docs.python.org/3/tutorial/venv.html
.. _venv2: https://docs.python.org/3/library/venv.html
.. _Sphinx: https://www.sphinx-doc.org/
.. _`Read the Docs`: https://readthedocs.org/
.. _`pigpio_download`: http://abyz.me.uk/rpi/pigpio/download.html
.. _pi_hotspot: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
.. _VNC: https://www.raspberrypi.org/documentation/remote-access/vnc/
.. _remote_pin : http://gpiozero.readthedocs.io/en/stable/remote_gpio.html
.. _ReStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _docs1: https://realpython.com/documenting-python-code/
.. _docs2: https://docs.python-guide.org/writing/documentation/
.. _docs3: https://www.youtube.com/watch?v=0ROZRNZkPS8
.. _docs4: https://www.youtube.com/watch?v=hM4I58TA72g
.. _pigpio_pi: http://abyz.me.uk/rpi/pigpio/python.html#pigpio.pi
