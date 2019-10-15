## Setting Up Your Local Database

You want to test your code locally before pushing to master, so how do you do this? (It might be worth mentioning that the above statement is not a question, it is, in fact a statement. You want to do this so that you don't push up broken code).

### High Level Overview

To do this you are going to need to SSH into the server, create a backup of the SQL database, and then retrieve that backup from your local machine. If you already have an RSA key, jump to creating a backup of the database below.

### Generating RSA Keys

To create this secure connection first you need to generate a pair of keys. If you are using a Mac or linux based system open your terminal, go to a folder where you would like to generate the keys and type in:
```
ssh-keygen -t rsa
```
It will prompt you to enter a file location so do this, then it will prompt you to enter a password. Leave the password blank (just press enter twice). Enter a key name WIHOUT an extension. Run ls to verify that you created two keys and you should see two files [yourkeyname] and [yourkeyname].pub.

### Putting Your RSA Key in the Server

When you are done generating your keys you need to put your public key into the server so that you can actually SSH in. If you don't know why this is necessary, research it. First read the contents of the public key by running
```
cat [yourkeyname].pub
```
Copy ALL of the text that shows up because this is important for later. Next open up your SSH into the server (ssh into backend, 162.222.176.13) that you created through the GCP website and type in the command:
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

Whenever you ^make changes to the database you need to create a backup first so that if things go to hell you can restore it. First go to one of your SSH's into the server. Change your directory into the nhs-server-backups folder. Then run the command:
```
mysqldump -p -u root nhs > backup-for-nhs-[year]-[month]-[date].sql
```
Replace [year], [month], and [date] with the correct values, eg 2019, 10, 08. Upon running this command type in the password for the database and when the command has finished running make sure that the file has been created.

### Retrieving Your Backup

Now you have to retrieve your backup, open up a terminal window and run the following command:
```
scp -i [yourkey] moundsviewnhs@162.222.176.13:~/nhs-server-backups/[name-of-backup] ~/[whatever-location]/[whatever-name].sql
```

### Setting up your SQL environment

Now that you have that sql file, you can use it to make a copy on your local machine. Open up a terminal window and run the command
```
mysql -u root -p
```
Enter your password then if you don't already have a schema for NHS run the command
```
create schema nhs;
```
Now add data to your schema. Exit the mysql instance then run the command
```
mysql -h localhost -u root nhs < [whatever-location]/[whatever-name].sql
```
And there you have it, nice job.
