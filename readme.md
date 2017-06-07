# Disclaimer
Please note this readme is intended for users that have little to no experience working with common Computer Science Technologies (ie command line, django, python, apis, etc).  Certain  steps have been embellished to allow for a wide range of audiences.
# Getting Started
Downloading and running the web application locally will require the use of command line inputs.  A step-by-step procedure has been outlined below.  Note, this is a common procedure when downloading from github.  
### Opening a commandline and confirming you have git
Open up a commandline on your computer.  For mac users the application is called Terminal.  Look for it in the application folder.  When initially prompted, confirm that you have a working version of git by typing

    git --version
    
into the command line.  You should see a response that tells you the version of git on your computer.  If you don't have git installed you will have to install it yourself.  For information on how you cann install git click [here](www.installgit.com).  For information about git itself is, click [here](https://www.atlassian.com/git/tutorials/what-is-git).
### Cloning from Github
To clone from github first navigate to your desktop folder.  This will be done using the 'cd' or change directory command.

    cd ~/Desktop
    
Now you can clone the url to your desktop.  Click on the 'Clone or Download' button on the located at the top right of all the listed files.  Copy the url in the description and type

    git clone <COPIED URL HERE>
    
The cursor should momentarily disappear and some text will display on the screen indicating the file is being downloaded.  When your cursor appears again you should see the text 'done' indicating that the project has been successfully downloaded.  There should be a folder titled Google-Analytics-Prediction-Application on your desktop.
### Running the Project
Back in terminal navigate to the project folder by typing

    cd ~/Desktop/Google-Analytics-Prediction-Application
    
Type the command
    
    ls

You should 2 items listed.  One folder titled prediction and one file named readme.md.  Navigate into the prediction folder.  Type ls again to ensure that you are in the right folder.  You should see several folders listed and one particular file titled 'manage.py'

    cd prediction
    ls
    
From here you will start the project by typing
    
    python manage.py runserver
    
You should see something like this 

![Alt clone_download](/tutorial_images/clone_download.jpg)

Open up the web browser of your choosing and type in the url in the folder.  This should take you to the homepage of the web application
    

    




