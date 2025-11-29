# Roku Movie Automation Agent

## What is this?

This is a computer program that automatically plays movies on the Roku Channel website. Instead of manually clicking play each time, this program does it for you automatically. It can play the same movie multiple times in a row, which is useful for testing or monitoring purposes.

**Think of it like:** A robot that clicks the "Play" button on your computer for you, over and over again.

## What does it do?

- 🎬 **Plays movies automatically** - The program opens the Roku Channel website and starts playing a movie without you needing to click anything
- 🔄 **Repeats automatically** - After a movie finishes, it can automatically start it again (you choose how many times)
- 📸 **Takes pictures** - The program can save screenshots (pictures of the screen) so you can see what happened if something goes wrong
- 📝 **Keeps a log** - It writes down everything it does in a text file, so you can check what happened later
- ⚙️ **Easy to customize** - You can change settings like which browser to use, how many times to repeat, and more
- 🛡️ **Handles errors** - If something goes wrong, the program tries to fix it automatically

## What do I need to use this?

### Your Computer
- **Mac computer** (macOS Monterey 12.7.3 or similar) - OR
- **Windows computer** (Windows 11 or similar)
- An internet connection

### Software to Install
You'll need to install a few free programs first:
1. **Python** - This is the programming language the program uses (version 3.8 or newer)
2. **Playwright** - This is a tool that lets the program control web browsers automatically

### Web Browser
The program works with these web browsers:
- **Mac**: Safari, Chrome, or Edge
- **Windows**: Chrome, Firefox, or Edge

**Note:** On Mac, Firefox doesn't work with this program, but it will automatically use Chrome instead if you try to use Firefox.

## How to Install (Step by Step)

### For Mac Users

#### Step 1: Get the Program Files
1. Download or copy all the program files to a folder on your computer (like your Desktop or Documents folder)

#### Step 2: Install Python (if you don't have it)
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or newer
3. Run the installer and follow the instructions
4. Make sure to check the box that says "Add Python to PATH" during installation

#### Step 3: Open Terminal
1. Press `Command + Space` to open Spotlight search
2. Type "Terminal" and press Enter
3. A black window will open - this is where you type commands

#### Step 4: Go to the Program Folder
1. In Terminal, type: `cd ` (with a space at the end)
2. Drag the folder containing the program files into the Terminal window
3. Press Enter

#### Step 5: Install Required Software
1. Type this command and press Enter:
   ```bash
   pip install -r requirements.txt
   ```
   This installs the tools the program needs to work.

2. Then type this command and press Enter:
   ```bash
   playwright install
   ```
   This downloads the web browsers the program will control.
   
   **Note:** You might see a message about "frozen ffmpeg browser" - this is normal and you can ignore it. It just means your Mac is using a stable version of the browser that works fine.

#### Step 6: (Optional) Set Up Safari
If you want to use Safari (the default Mac browser):
1. Open Safari
2. Click "Safari" in the menu bar at the top
3. Click "Preferences" (or "Settings" on newer Macs)
4. Click the "Advanced" tab
5. Check the box that says "Show Develop menu in menu bar"
6. Close the Preferences window
7. Click "Develop" in the menu bar (it should appear now)
8. Click "Allow Remote Automation"

### For Windows Users

#### Step 1: Get the Program Files
1. Download or copy all the program files to a folder on your computer (like your Desktop or Documents folder)

#### Step 2: Install Python (if you don't have it)
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or newer
3. Run the installer
4. **Important:** Check the box that says "Add Python to PATH" during installation
5. Click "Install Now"

#### Step 3: Open PowerShell or Command Prompt
1. Press the Windows key
2. Type "PowerShell" or "Command Prompt"
3. Right-click on it and select "Run as Administrator" (this gives you permission to install things)
4. Click "Yes" if Windows asks for permission

#### Step 4: Go to the Program Folder
1. In PowerShell/Command Prompt, type: `cd ` (with a space at the end)
2. Navigate to your program folder. For example, if it's on your Desktop:
   ```powershell
   cd C:\Users\YourName\Desktop\Agentic_Roku
   ```
   (Replace "YourName" with your actual Windows username)

#### Step 5: Install Required Software
1. Type this command and press Enter:
   ```powershell
   pip install -r requirements.txt
   ```
   Wait for it to finish installing.

2. Then type this command and press Enter:
   ```powershell
   playwright install
   ```
   This will download the web browsers. It might take a few minutes.

#### Step 6: (If You Get Permission Errors)
If Windows blocks something:
1. Make sure you're running PowerShell/Command Prompt as Administrator (see Step 3)
2. In PowerShell, you might need to type this first:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```
   Type "Y" and press Enter if it asks for confirmation

**Note:** Safari is not available on Windows. The program will use Chrome, Firefox, or Edge instead.

## How to Use the Program

### Simple Way (Easiest)

1. Open Terminal (Mac) or PowerShell/Command Prompt (Windows)
2. Make sure you're in the program folder (see Installation steps above)
3. Type this command and press Enter:
   ```bash
   python main.py
   ```
   
   This will:
   - Open a web browser automatically
   - Go to the Roku Channel website
   - Play the movie 5 times in a row
   - Wait 5 seconds between each play

### Customizing How It Works

You can change how the program behaves by adding options to the command:

**Play the movie more times:**
```bash
python main.py --max-loops 10
```
(This plays the movie 10 times instead of 5)

**Wait longer between plays:**
```bash
python main.py --loop-delay 10
```
(This waits 10 seconds between each play instead of 5)

**Use a specific browser:**
```bash
# Mac - Use Safari
python main.py --browser safari

# Mac or Windows - Use Chrome
python main.py --browser chrome

# Windows - Use Edge
python main.py --browser edge
```

**Play forever (until you stop it):**
```bash
python main.py --max-loops -1
```
(Press Ctrl+C to stop it)

**Run without showing the browser window:**
```bash
python main.py --headless
```
(This runs in the background - you won't see the browser, but it still works)

**Run slower (easier to see what's happening):**
```bash
python main.py --slow-mo 1000
```
(This makes everything happen 1 second slower, so you can watch what's happening)

### Advanced: Using Settings Files

Instead of typing options every time, you can set them once using environment variables. This is optional - most people don't need this.

**On Mac:**
```bash
export MAX_LOOPS=10
export LOOP_DELAY=5
export BROWSER=safari
python main.py
```

**On Windows (PowerShell):**
```powershell
$env:MAX_LOOPS=10
$env:LOOP_DELAY=5
$env:BROWSER=chrome
python main.py
```

**On Windows (Command Prompt):**
```cmd
set MAX_LOOPS=10
set LOOP_DELAY=5
set BROWSER=chrome
python main.py
```

### What Do All These Options Mean?

- `--max-loops`: How many times to play the movie (use -1 to play forever)
- `--loop-delay`: How many seconds to wait between each play
- `--browser`: Which web browser to use (safari, chrome, firefox, or edge)
- `--headless`: Run without showing the browser window (runs in background)
- `--slow-mo`: Make everything slower so you can watch what's happening (number is in milliseconds, so 1000 = 1 second slower)
- `--log-level`: How much information to save in the log file (DEBUG = lots of info, ERROR = only errors)

## Changing Settings in the Config File

If you want to change the default movie or other settings permanently, you can edit the `config.py` file. This is optional - most people use the command line options instead.

You can change:
- Which movie to play (the URL/website address)
- Default browser
- How long to wait for things to load
- Where to save screenshots

**Note:** Only edit this file if you're comfortable editing code. If you're not sure, just use the command line options instead.

## What Files Does the Program Create?

When you run the program, it creates:

1. **`roku_automation.log`** - A text file that records everything the program did. Useful if something goes wrong and you need to figure out what happened.

2. **`screenshots/` folder** - A folder containing pictures of the screen at different points. These help you see what the program was doing.

3. **Messages on screen** - The program will show you what it's doing in real-time as it runs.

## Problems and Solutions

### Common Issues on Mac

1. **Safari won't work / "Safari not responding"**
   - **Solution:** Make sure Safari automation is turned on:
     - Open Safari
     - Click "Safari" → "Preferences" → "Advanced" tab
     - Check "Show Develop menu in menu bar"
     - Click "Develop" → "Allow Remote Automation"

2. **Warning message about "frozen ffmpeg browser"**
   - **What it means:** This is just a message saying your Mac is using a stable browser version
   - **Solution:** You can ignore this - it's not a problem, the program will still work fine

3. **Error about "autoplay permission"**
   - **What it means:** Safari handles video playback differently than other browsers
   - **Solution:** The program handles this automatically - you don't need to do anything

4. **Error with long technical name like "FixedBackgroundsPaint..."**
   - **What it means:** Sometimes Safari and the automation tool don't work perfectly together
   - **Solution:** The program tries to fix this automatically. If it keeps happening, try updating the tools:
     ```bash
     pip install --upgrade playwright
     playwright install
     ```

5. **Browser won't start**
   - **Solution:** The program will automatically try using Chrome instead of Safari

6. **Firefox doesn't work**
   - **What it means:** Firefox isn't supported on Mac with this program
   - **Solution:** The program will automatically use Chrome instead

7. **Chrome gives an error about "incognito mode"**
   - **What it means:** Chrome's private browsing mode doesn't work with this program
   - **Solution:** The program automatically uses a different mode - you don't need to do anything

8. **Roku Channel blocks Chrome**
   - **What it means:** Sometimes the Roku website doesn't work well with Chrome on Mac
   - **Solution:** Use Safari instead: `python main.py --browser safari`

### Common Issues on Windows

1. **"Permission denied" or "Access denied" errors**
   - **Solution:** Make sure you're running PowerShell or Command Prompt as Administrator:
     - Right-click on PowerShell/Command Prompt
     - Select "Run as Administrator"
     - Click "Yes" when Windows asks for permission
   - Also check that Windows Defender or your antivirus isn't blocking the program

2. **"Browser not found" error**
   - **Solution:** Make sure the browsers are installed:
     ```powershell
     playwright install
     ```
   - Also make sure you have Chrome, Edge, or Firefox installed on your computer

3. **"Script execution blocked" error**
   - **Solution:** In PowerShell, type this command:
     ```powershell
     Set-ExecutionPolicy RemoteSigned
     ```
     Type "Y" and press Enter if it asks for confirmation

### Problems That Can Happen on Any Computer

4. **"Element not found" error**
   - **What it means:** The Roku website might have changed, so the program can't find the play button
   - **Solution:** The website might have been updated. Check if you can manually play a movie on the website first

5. **"Timeout" errors**
   - **What it means:** The program waited too long for something to happen
   - **Solution:** Your internet might be slow, or the website might be loading slowly. Try again later

6. **"Permission denied" error**
   - **What it means:** The program doesn't have permission to control the browser
   - **Solution:** Make sure you followed all the installation steps, especially enabling browser automation

### Which Browser Should I Use?

#### For Mac Users

**Best choice:** Safari
- Works best with the Roku Channel website
- Usually the most reliable

**If Safari doesn't work:** Chrome
- The program will automatically use Chrome if Safari fails
- Note: Sometimes Roku Channel blocks Chrome on Mac, so Safari is usually better

**Don't use:** Firefox
- Firefox doesn't work with this program on Mac
- The program will automatically switch to Chrome if you try to use Firefox

#### For Windows Users

**Best choices (all work well):**
1. **Chrome** - Usually works best
2. **Edge** - Windows' built-in browser, also works great
3. **Firefox** - Also works fine

**Can't use:** Safari
- Safari isn't available on Windows
- The program will automatically use Chrome instead

### Getting More Information (Debug Mode)

If something isn't working and you want to see more details about what's happening:

```bash
python main.py --log-level DEBUG
```

This will show you a lot more information about what the program is doing, which can help figure out what went wrong.

## Technical Details (For Those Who Are Curious)

This program uses a tool called **Playwright** to control web browsers. Playwright is like a remote control for web browsers - it can open browsers, click buttons, fill in forms, and do other things automatically.

**Why Playwright?**
- It's modern and works with current websites
- It works with multiple browsers (Safari, Chrome, Firefox, Edge)
- It's easier to set up than older tools
- It's actively maintained and updated
- It's faster and more reliable than alternatives

## Important Legal Information

**This program is for educational and testing purposes only.**

Please make sure you:
- Follow Roku's Terms of Service (the rules for using their website)
- Follow your local laws and regulations
- Use the program responsibly and ethically

**What this means:** Don't use this program to do anything that violates Roku's rules or breaks any laws. Use it only for legitimate testing or learning purposes.

## Getting Help

If you have problems or questions:
- Check the "Problems and Solutions" section above
- Look at the log file (`roku_automation.log`) to see what happened
- Check the screenshots folder to see what the program was doing

## Want to Help Improve This Program?

If you find problems or have ideas for improvements, feel free to share them! This helps make the program better for everyone.

---

**Remember:** This is an educational tool. Use it responsibly and make sure you're following all applicable rules and laws.
