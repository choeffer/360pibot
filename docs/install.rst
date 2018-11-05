.. _Installation:

Installation
============

The following steps to set up a working environment are valid for both, 
the Raspberry Pi and a laptop/computer. 
Remember, the modules can be used on a laptop/computer for remote controlling 
the Raspberry Pis GPIOs or on the Raspberry Pi itself without any modifications 
of the source code of the modules. On the Raspberry Pi, the latest Raspbian 
version and afterwards all available updates should be installed. The latest 
Raspbian image can be downladed from `Raspbian Downloads`_ . Installing all 
available updates is described here `Raspbian Update`_ .

Getting files
-------------

One option is creating a folder named ``360pibot`` in the Raspberry Pis ``home`` 
folder

.. code-block:: console

    cd ~
    mkdir 360pibot

and then connect the Raspberry Pi to the internet, open the projects github page, 
download the repository as a .zip file and unzip it in the created ``360pibot`` 
folder.

Another option is to clone the git repository to the ``home`` folder. 
This will automatically create the ``360pibot`` folder and download the project 
files. First, git will be installed, then the repository 
will be cloned.

.. code-block:: console

    sudo apt-get update
    sudo apt-get install git
    cd ~
    git clone https://github.com/choeffer/360pibot

Both methods for getting the project files are also working on a laptop/computer.

Installing needed modules
-------------------------

Next step is to install the needed modules. They can be installed in the global 
Python 3 environment or in a virtual Python 3 environment. The latter has the 
advantage that the packages are isolated from other projects and also from the 
system wide installed global once. If things get messed up, the virtual 
environment can just be deleted and created from scratch again. For more 
informations about virtual environments in Python 3, see venv1_ and venv2_ . 
First, installing with a virtual environment will be explainend, afterwards 
with using the global Python 3 environment.

With a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

On a Raspberry Pi first ensure that the packages ``python3-venv`` and ``python3-pip`` 
are installed. This has also to be checked on Debian based distributions like 
Ubuntu/Mint. 

.. code-block:: console

    sudo apt-get update
    sudo apt-get install python3-venv python3-pip

Afterwards, navigate to the created ``360pibot`` folder and create a virtual 
environment named ``venv`` and activate it. An activated virtual environment 
is indicated by a ``(venv)`` in the beginning of the terminal prompt.

.. note::

    The created ``venv`` folder is added to the .gitignore file and will therefore 
    not be tracked by git.

.. code-block:: console

    cd ~
    cd 360pibot
    python3 -m venv venv
    source venv/bin/activate

With the activated virtual environment install the needed ``pigpio`` module inside.

.. code-block:: console

    pip3 install pigpio

Deactivating the acvtivated virtual environment can be done later by just typing 
``deactivate`` in the terminal where the virtual environment is activated.

.. code-block:: console

    deactivate

.. note::

    For later using the installed module, the virtual environment has to be activated, 
    because the pigpio package is installed inside and is not callable from the 
    global Python 3 environment.

Without a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On a Raspberry Pi first ensure that the package ``python3-pip`` 
is installed. This has also to be checked on Debian based distributions like 
Ubuntu/Mint. Then, the ``pigpio`` module will be installed in the global 
Python 3 environment.

.. code-block:: console

    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install pigpio


Building/modifying the documentation
------------------------------------

The whole documentation is made with Sphinx_ and can be extended or 
modified as needed for e.g. documenting own projects based on this or if 
extending functionality of the modules and documenting this. The whole 
documentation is stored in the ``docs/`` folder. The standard 
docstring format (ReStructuredText_ (reST)) is used. The used 
theme is from `Read the Docs`_ where also the documentation is hosted. 
Therefore, two more modules are needed for beeing able to build or extend/modify 
the documentation. How to use Sphinx is not part of this documentation. 
But there are good introductions and tutorials available which provide a good starting 
point, see docs1_ , docs2_ , docs3_ and docs4_ .

.. note::

    For the creation of the docs ``conf.py`` , ``index.rst`` , and folder structure etc. 
    the ``sphinx-quickstart`` command was used.

.. note::

    The created ``docs/_build`` folder is added to the .gitignore file and will therefore 
    not be tracked by git. This folder contains the output after building the docs.

If using a virtual environment to install the two modules

.. code-block:: console

    cd ~
    cd 360pibot
    source venv/bin/activate
    pip3 install sphinx sphinx_rtd_theme

or if installing them in the global Python 3 environment.

.. code-block:: console

    pip3 install sphinx sphinx_rtd_theme

After this, the following command ``make html`` builds the html documentation 
which will be stored in the ``docs/_build/html/`` folder. There, open the 
``index.html`` with your preferred web browser.

If using a virtual environment

.. code-block:: console

    cd ~
    cd 360pibot
    source venv/bin/activate
    cd docs
    make html

or if using the global Python 3 environment.

.. code-block:: console

    cd ~
    cd 360pibot/docs
    make html

Sphinx can create the documentation in different formats (e.g. latex, html ,pdf, epub), 
see `sphinx-build`_ for more informations.

Used module versions
--------------------

The ``requirements.txt`` file will install the exact versions of 
the modules which are used while experimenting/developing with 
the demo implementation and writing the documentation.

This can be done by using a virtual environment

.. code-block:: console

    cd ~
    cd 360pibot
    source venv/bin/activate
    pip3 install -r requirements.txt

or by installing them in the global Python 3 environment.

.. code-block:: console

    pip3 install -r requirements.txt

The ``requirements.txt`` file is created with ``pip3 freeze > requirements.txt``. 
The ``requirements_rtd.txt`` file is used by `Read the Docs`_ . The online version 
of the documentation is auto build/updated each time a ``git push`` is made to 
the github repository. For further information, see `Read the Docs Webhooks`_ .

Raspberry Pi
------------

The following steps are specific to the Raspberry Pi. It is necessary to install the 
``pigpio`` package, enable starting the pigpio daemon at boot and then doing a reboot 
to activate the pigpio daemon. For more information see `pigpio_download`_  and remote_pin_ . 
For the demo implementation the package from the Raspbian repository is installed. 
This ensures that the package is good integrated in the system, even if it might be a 
bit older.

.. code-block:: console

    sudo apt-get update
    sudo apt-get install pigpio
    sudo systemctl enable pigpiod
    sudo reboot

.. note::

    If the Raspberry Pis GPIOs are not responding anymore, it might help to restart the
    pigpio daemon on the Raspberry Pi. For that, SSH into the Raspberry Pi if 
    remotely working with it, otherwise use the local terminal, and execute the 
    following two commands.

    .. code-block:: console

        sudo systemctl daemon-reload
        sudo systemctl restart pigpiod.service

Hotspot and remote access
^^^^^^^^^^^^^^^^^^^^^^^^^

An important step which improves programming/controlling the Raspberry Pi is to make it remotely 
accessable. This can be done by connecting the Raspberry Pi to a WLAN network or by 
enabling a hotspot on it, see pi_hotspot_ . This is recommended 
before using it. Setting up a hotspot will not be covered here, because the official documentation 
is good and updated regularly to match the latest Raspbian changes.

Also make yourself familiar with using VNC_ or using remote_pin_ . Latter will again 
drastically improve the use of the modules, because then all programming/controlling can 
be done on a laptop/computer inlcuding using an IDE, having much more system ressources 
and so on. The latter option is shortly described.

After enabling a hotspot on the Raspberry Pi and beeing connected with your 
laptop/computer, the following steps are needed to remote control the 
Raspberry Pis GPIOs. For a more detailed description, see remote_pin_ .

First, in the Raspberry Pi configuration *Remote GPIO* has to be enabled. This can 
be done via GUI or ``sudo raspi-config``. This will allow remote connections while 
the pigpio daemon is running.

Then, the environment variable has to be set while or before launching Python 3 or an IDE. 
This variable will point to the IP address (and optional port) on which the Raspberry Pi 
is accessable. This can be on its own provided hotspot/network or on a WLAN it is connected to. 

.. code-block:: console

    PIGPIO_ADDR=192.168.1.3 python3 hello.py
    PIGPIO_ADDR=192.168.1.3 python3 code .

There are also other possibilities available for configuring remote access. They are 
mentioned in the pigpio documentation, see pigpio_pi_ . E.g. the IP address and port 
can be passed as arguments if initializing a pigpio.pi() instance.

References
----------

.. target-notes::

.. _`Raspbian Downloads`: https://www.raspberrypi.org/downloads/raspbian/
.. _`Raspbian Update`: https://www.raspberrypi.org/documentation/raspbian/updating.md
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
.. _`Read the Docs Webhooks`: https://docs.readthedocs.io/en/latest/webhooks.html
.. _`sphinx-build`: http://www.sphinx-doc.org/en/master/man/sphinx-build.html#cmdoption-sphinx-build-b