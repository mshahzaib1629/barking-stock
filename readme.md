# Barking Stock

Barking Stock monitors Companies announcements at PSX Stock Market and notify all the subscribers about the updates of their favorite companies.

## Table of Contents

1. [Clonning Project and Initial Setup](#clonning-project-and-initial-setup)
2. [Conda Installation & Environment Creation](#conda-installation--environment-creation)
3. [Package Installation using `requirements.txt`](#package-installation-using-requirementstxt)
4. [Guide for Downloading & Installing Chrome](#guide-for-downloading--installing-chrome)
5. [Running the App Manually](#running-the-app-manually-optional-but-recommended)
6. [Setup Log File and Executionable Script](setup-log-file-and-executionable-script)
7. [Scheduling Executionable Script using Crontab](#scheduling-executionable-script-using-crontab)

## Clonning Project and Initial Setup

Login to the Server and set SSH key.

```sh
ssh-keygen -t ed25519 -b 256
```

Copy the public key to the Access keys of project, and clone the project into server.

```sh
git clone git@github.com:mshahzaib1629/barking-stock.git
```

## Conda Installation & Environment Creation

1. **Install Conda**
   
   Download the Miniconda installer directly from the official Miniconda website using wget or curl. Make sure to download the installer for your system architecture (usually x86_64 for most servers).

   ```sh
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```

   Alternatively, use curl:

   ```sh
   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```
   
   Make the installer executable and run it:

   ```sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```
   
   Review and accept the license agreement by pressing Enter until you reach the end of the agreement, then type yes.
   Choose the installation location (the default is typically ~/miniconda3).
   
   When prompted, confirm the installation location or specify a different one.

   Restart your shell session or run:

   ```sh
   source ~/.bashrc
   ```

   After installation, you can delete the Miniconda installer script:

   ```sh
   rm Miniconda3-latest-Linux-x86_64.sh
   ```
       
3. **Create a new Conda environment**

   Create a conda environment named `barking-stock` with python version 3.12.4

   ```sh
   conda create -n barking-stock python=3.12.4
   ```

## Package Installation using `requirements.txt`

   ```sh
   conda activate barking-stock
   ```
   
   Now install all the required packages.
   
   ```sh
   pip install -r requirements.txt
   ```

   Ensure that the requirements.txt file is in the root directory of your project.

## Guide for Downloading & Installing Chrome

Download the Google Chrome

```sh
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

Install the Google Chrome

```sh
sudo apt install ./google-chrome-stable_current_amd64.deb
```

After installing, we can delete .deb file

```sh
rm ./google-chrome-stable_current_amd64.deb
```

## Running the App Manually (Optional, but Recommended)

To get the chromedriver, we need to run the app manually for the first time. By running the following command, the code will be executed and chrome driver will be installed.

```sh
python main.py
```

Now you'll have chromedriver file at `/home/<YourUsername>/.wdm/drivers/chromedriver/<version>`.

We can copy that file into the `/path/to/barking-stock/chrome-driver/`

```sh
cp /home/<YourUsername>/.wdm/drivers/chromedriver/<version> /path/to/barking-stock/chrome-driver/
```

## Setup Log File and Executionable Script

To store the logs, we need a log file in the project root directory.

```sh
touch crontab.log
```

Create a shell script `starter_script.sh` by using command `touch starter_script.sh` and add the following script in it:

```sh
#!/bin/bash
echo -e "Script started at: $(date)\n--------------------------------------------------\n" >> /path/to/barking-stock/crontab.log

source /home/<YourUsername>/miniconda3/bin/activate barking-stock  # Activate the conda environment
python /path/to/barking-stock/main.py

echo -e "\nScript ended at: $(date)\n\n--------------------------------------------------" >> /path/to/barking-stock/crontab.log
```

Remember to replace the `path/to/barking-stock/' with the actual project path.

And make sure the script is executable.

```sh
chmod +x /path/to/barking-stock/starter_script.sh
```

## Scheduling Executionable Script using Crontab

We can set `starter_script.sh` to run as a regular job by adding it in linux crontab.

Open the crontab by using following command:

```sh
crontab -e
```

At the end of the file, add the following line to execute `starter_script.sh` after every 1 minute.

```sh
* * * * * /path/to/barking-stock/starter_script.sh >> /path/to/barking-stock/crontab.log 2>&1
```

This command will execute the `starter_script.sh` after every 1 minute and write the logs into the crontab.log file inside the project root.

To set the job to execute every 1 hour, replace the * * * * * with the following pattern:

```sh
0 * * * *
```

To set the job to execute every hour from 8 AM to 5 PM, Monday through Friday, replace the pattern with:

```sh
0 8-17 * * 1-5
```
