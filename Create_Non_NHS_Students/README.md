## How to Add Students to Server

### Description

This folder is dedicated towards having an automated method of adding students to the MySQL server and making sure that everyone has logged in correctly.

## Basic Instructions

To run this script you need to SSH into the server and use port forwarding to run commands through this SSH. If you don't know what SSH is watch this [video](https://www.youtube.com/watch?v=z7jVOenqFYk). Basically it allows you to communicate directly with the server from your local terminal by creating a secure connection. Port forwarding essentially allows you to pipe stuff through this connection.

### Generating RSA Keys

To create this secure connection first you need to generate a pair of keys. If you are using a Mac or linux based system open your terminal, go to a folder where you would like to generate the keys and type in:
```
ssh-keygen -t rsa
```
It will prompt you to enter a file name so do this, then it will prompt you to enter a password. Leave the password blank (just press enter twice). Run ls to verify that you created two keys and you should see two files [yourkeyname] and [yourkeyname].pub.

### Putting Your RSA Key in the Server

When you are done generating your keys you need to put your public key into the server so that you can actually SSH in. If you don't know why this is necessary, research it. First read the contents of the public key by running
```
cat [yourkeyname].pub
```
Copy the text that shows up this is important for later. Next open up your SSH into the server that you created through the GCP website and type in the command:
```
vim .ssh/authorized_keys
```
Once you run this you should see a list of different keys. Copy paste your key into the list on a new line then save the file. If you don't know how to use vim look it up.

### Creating the Secure Connection

Open up your terminal on your local machine and cd into the file with your keys. Run the command:
```
ssh -i [yourkeyname] moundsviewnhs@162.222.176.13
```
You should be in now. Verify that you are in by looking towards the left side of your terminal for something like:
```
moundsviewnhs@instance-1
```
Showing that you are logged in as that user.

### Creating a Backup of the Database

Whenever you make changes to the database you need to create a backup first so that if things go to hell you can restore it. First go to one of your SSH's into the server. Change your directory into the nhs-server-backups folder. Then run the command:
```
mysqldump -p -u root nhs > backup-for-nhs-[year]-[month]-[date].sql
```
Replace [year], [month], and [date] with the correct values, eg 2019, 10, 08. Upon running this command type in the password for the database and when the command has finished running make sure that the file has been created.

### Setting up the Script

To actually run the script you need to have some data to insert into the database. Go to Google Sheets and create a list of students in NHS with the columns First Name, Last Name, and Email. Fill in the correct information for these columns then export this as a csv file. Look in the lib folder and you should see a members.csv file. Replace this file with the csv file you just generated (make sure to call it members.csv and remove the original file).

### Testing the Script Locally

It is very important that you don't mess stuff up. To make sure that you don't it is good practice to run the script locally. This is pretty easy. First simulate the environment. To do this you need to bring down the sql database from the server onto your machine. You are going to be copying the backup that you created earlier. Run the command
```
scp -i [yourkey] moundsviewnhs@162.222.176.13:~/nhs-server-backups/[name-of-backup] ~/Documents/[something].sql
```
Now close the SSH connection that you have (press control-D or close the window). This is very important because you don't want to accidentally run it on the server so it is safest to close it. Now configure the script for running locally. Change the passwords, delete the bit about the port and MAKE SURE IT DOESN'T EMAIL ANYBODY.
Now setup your local SQL database to emulate the server's by running the following command in your terminal:
```
mysql -h localhost -u root nhs < [something].sql
```
Now you can run the script. Verify that it DOES NOT EMAIL ANYBODY YET. To run the script, execute addstudents.py and visit the local address it gives you. After doing this check on your local SQL database and make sure that it behaved as predicted. After all of this revert the code to run on the server and reopen your SSH connection.

### Running the Script

To run the script open up your terminal. In the window that is connected to the server run the command
```
top
```
This is a basic command that will make sure that your connection doesn't time out. It doesn't do anything important (basically an activity monitor). Then open a new window not SSH'd in and cd into this folder. Run
```
python addstudents.py
```
This locally hosts a server which when visited runs the script. This is a super jank way to do it but because of the way Flask works it was the easiest. Anyways after doing this visit whatever URL that terminal is telling you is hosting it (prolly like 127.0.0.1:5000/ or something). Then go back to your terminal and you should see the results of the script begin to show up. This script takes a LONG time to run because of the emails it needs to send. While this script is running watch the terminal logs to make sure that everything is going well. There shouldn't be errors, but if there are, figure it out lol.

### If Everything Goes To Hell

If the script messes everything up, apologize for the emails sent then ssh into the server and reset the database to the backup your created.
```
mysql -h localhost -u root nhs < [name of the sql dump you created ealier]
```
Really you shouldn't have to do this, check everything before you run the script of course...
