# Control LG TV OLED C2

# 1 - Setting up the environment:

## Requirements:

- **Git** of course :-)
- **pyenv-virtualenv** :

  - Mac OS:

    1. Install **Homebrew** ([install](https://brew.sh/))

    1. Install package:
       ```sh
       brew install pyenv-virtualenv
       ```
    1. Add it to path (assuming you are using ZSH)
       ```sh
       echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
       ```
       ```sh
       echo 'eval "$(pyenv init -)"' >> ~/.zshrc
       ```
       ```sh
       echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
       ```

  - Other OS:
    ([Follow instructions to install](https://github.com/pyenv/pyenv-virtualenv))

<br/>
<br/>

## Configuration Steps:

1. Clone the repo

   ```sh
   git clone git@github.com:rockorama/lgtv.git
   ```

   and then:

   ```sh
   cd lgtv
   ```

1. Install python version

   ```sh
   pyenv install 3.10.0
   ```

1. Create the Python virtual environment (Only needed once)

   ```sh
   pyenv virtualenv 3.10.0 lgtv

   ```

1. Update PIP
   ```sh
   pip install -U pip
   ```
1. Install Vyper Dependencies

   ```sh
   pip install -r requirements.txt
   ```

## Update your settings:

Copy the `.env-example` file and rename it to `.env` then change the settings to apply to your TV:
```
IP=192.168.68.99 # -->> THE IP OF YOUR TV
INPUT=HDMI_1
INPUT_MODE=pc
INPUT_NAME=Mac
```

## Run the script

   ```sh
   python ./control-tv.py
   ```


To run your Python script at startup on a Mac, you can use a few different methods. The most common and straightforward ways are:

1. **Using Automator to Create an Application (Recommended)***:
   - Open Automator (found in your Applications folder).
   - Choose to create a new 'Application'.
   - In the search pane, type 'shell' and drag 'Run Shell Script' into the workflow on the right.
   - In the shell script box, enter the command to run your Python script. For example: `~/.pyenv/versions/3.10.0/envs/lgtv/bin/python ~/Projects/lgtv/control-tv.py`.
   - Save your application (e.g., `ControlLGTV.app`) in a location of your choice.
   - Open System Preferences > Users & Groups.
   - Select your user account and go to the 'Login Items' tab.
   - Click the '+' button and select the application you created in Automator.

2. **Using a PLIST file to create a Launch Agent**:
   - Create a new PLIST file (e.g., `com.yourname.scriptname.plist`) in `~/Library/LaunchAgents`. You can do this using a text editor.
   - Fill the PLIST file with the appropriate configuration. A basic template would look like this:
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
     <plist version="1.0">
     <dict>
         <key>Label</key>
         <string>com.yourname.scriptname</string>
         <key>ProgramArguments</key>
         <array>
             <string>/usr/bin/env</string>
             <string>python3</string>
             <string>/path/to/your/script.py</string>
         </array>
         <key>RunAtLoad</key>
         <true/>
     </dict>
     </plist>
     ```
   - Make sure to replace `/path/to/your/script.py` with the actual path to your Python script.
   - Load the new agent with the command: `launchctl load ~/Library/LaunchAgents/com.yourname.scriptname.plist`.
   - To have it start automatically at login, you may need to log out and log back in or restart your Mac.

3. **Using crontab**:
   - Open Terminal.
   - Type `crontab -e` to edit the cron jobs.
   - Add a line like `@reboot /usr/bin/env python3 /path/to/your/script.py`.
   - Save and exit the editor.

Remember to replace `/path/to/your/script.py` with the actual path to your script and ensure that your script has the correct executable permissions (`chmod +x script.py`). Also, if your script requires administrator privileges, additional steps may be necessary. 

Each method has its pros and cons, so choose the one that best fits your needs and comfort level with macOS system administration.