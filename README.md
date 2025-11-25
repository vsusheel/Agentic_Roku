# Roku Movie Automation Agent

An agentic workflow application that automates playing movies on the Roku channel web interface using Playwright with cross-platform support (macOS Monterey 12.7.3 and Windows 11).

## Features

- 🎬 Automated movie playback on Roku channel
- 🔄 Configurable looping functionality
- 📸 Screenshot capture for debugging
- 📝 Comprehensive logging
- ⚙️ Environment-based configuration
- 🛡️ Error handling and recovery

## Prerequisites

- **macOS** (tested on macOS Monterey 12.7.3) - supports Safari, Firefox, Chrome/Chromium, Edge
- **Windows 11** (tested on Windows 11) - supports Chrome, Firefox, Edge
- Python 3.8+
- Playwright browsers installed

## Installation

### macOS Monterey 12.7.3

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install
   ```

4. (Optional) Enable Safari for automation:
   - Open Safari
   - Go to Safari > Preferences > Advanced
   - Check "Show Develop menu in menu bar"
   - Go to Develop > Allow Remote Automation

### Windows 11

1. Clone or download this repository
2. Open PowerShell or Command Prompt as Administrator (recommended)
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```powershell
   playwright install
   ```

5. (Optional) If you encounter permission issues, you may need to:
   - Run PowerShell/CMD as Administrator
   - Allow script execution: `Set-ExecutionPolicy RemoteSigned` (PowerShell)
   - Ensure Windows Defender or antivirus allows Playwright browser downloads

**Note:** Safari is not available on Windows. Use Chrome, Firefox, or Edge instead.

## Usage

### Basic Usage

```bash
# Run with default settings (5 loops)
python main.py

# Run with custom settings
python main.py --max-loops 10 --loop-delay 10 --browser safari

# Run with Chrome/Chromium on macOS (Firefox not supported, will auto-fallback to Chrome)
python main.py --browser chrome

# Run with Chrome (note: may be blocked by Roku Channel on macOS)
python main.py --browser chrome

# Windows 11 - Run with Chrome (recommended for Windows)
python main.py --browser chrome

# Windows 11 - Run with Edge (native Windows browser)
python main.py --browser edge

# Windows 11 - Run with Firefox
python main.py --browser firefox

# Run in headless mode
python main.py --headless

# Run with slow motion for debugging
python main.py --slow-mo 1000

# Run infinite loops
python main.py --max-loops -1
```

### Configuration

You can configure the automation using environment variables or command line arguments:

```bash
# macOS/Linux - Using environment variables
export MAX_LOOPS=10
export LOOP_DELAY=5
export BROWSER=safari
python main.py
```

```powershell
# Windows 11 - Using environment variables (PowerShell)
$env:MAX_LOOPS=10
$env:LOOP_DELAY=5
$env:BROWSER=chrome
python main.py
```

```cmd
# Windows 11 - Using environment variables (CMD)
set MAX_LOOPS=10
set LOOP_DELAY=5
set BROWSER=chrome
python main.py
```

### Command Line Options

- `--max-loops`: Maximum number of loops (-1 for infinite)
- `--loop-delay`: Delay between loops in seconds
- `--browser`: Browser to use (safari, chrome, firefox, edge)
- `--headless`: Run browser in headless mode
- `--slow-mo`: Slow down operations by specified milliseconds
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Configuration File

The application uses `config.py` for default settings. You can modify:

- Movie URL
- Browser settings
- Timeout values
- Selector patterns
- Screenshot settings

## Output

The application creates:

- `roku_automation.log`: Detailed execution log
- `screenshots/`: Screenshots for debugging
- Console output with real-time status

## Troubleshooting

### Common Issues

#### macOS Monterey 12.7.3

1. **Safari not responding**: Ensure Safari automation is enabled
   - Safari > Preferences > Advanced > Enable "Show Develop menu"
   - Develop > Allow Remote Automation
2. **Safari autoplay permission error**: Safari/WebKit doesn't support the 'autoplay' permission API. The automation automatically skips permission grants for Safari - this is normal and won't affect functionality.
3. **Safari "FixedBackgroundsPaintRelativeTo Document" error**: This is a known Playwright compatibility issue with Safari/WebKit. The automation automatically handles this error by:
   - Catching the error and retrying page creation
   - Using existing pages from the context if available
   - If the issue persists, try updating Playwright: `pip install --upgrade playwright && playwright install`
4. **Browser launch failed**: The automation will automatically fall back to Chrome/Chromium if Safari fails
5. **Firefox not supported**: Playwright's Firefox browser is not supported on macOS. If you specify Firefox, the automation will automatically fall back to Chrome/Chromium.
6. **Chrome incognito mode error**: Chrome in incognito mode is not supported on macOS. The automation automatically uses a persistent context instead of incognito mode to avoid this issue.
7. **Chrome/Chromium blocked by Roku**: Roku Channel may block Chrome on macOS. Use Safari instead if Chrome is blocked.

#### Windows 11

1. **Permission denied errors**: 
   - Run PowerShell/CMD as Administrator
   - Check Windows Defender exclusions for Playwright browsers
   - Ensure antivirus isn't blocking browser downloads
2. **Browser not found**: 
   - Run `playwright install` to ensure browsers are installed
   - Check that Chrome/Edge/Firefox are installed on your system
3. **Script execution blocked**:
   - PowerShell: Run `Set-ExecutionPolicy RemoteSigned`
   - Or run: `python -m playwright install` directly

#### Cross-Platform

4. **Element not found**: The page structure may have changed
5. **Timeout errors**: Increase timeout values in config
6. **Permission denied**: Check browser automation permissions

### Platform Compatibility

#### macOS Monterey 12.7.3

This automation has been optimized for macOS Monterey 12.7.3:

- ✅ **Safari (WebKit)**: Primary browser with automatic fallback if unavailable
- ❌ **Firefox**: Not supported by Playwright on macOS (automatically falls back to Chrome)
- ✅ **Chrome/Chromium**: Supported, automatically used as fallback for Safari/Firefox
- ✅ **Edge**: Supported via Chromium engine

**Recommended browsers for macOS Monterey:**
1. **Safari** (best compatibility with Roku Channel)
2. **Chrome/Chromium** (reliable fallback, automatically used if Safari fails or Firefox is requested)
3. Edge (may show browser compatibility warnings)

**Note:** If you specify Firefox on macOS, the automation will automatically use Chrome/Chromium instead, as Playwright's Firefox is not supported on macOS.

#### Windows 11

This automation has been optimized for Windows 11:

- ✅ **Chrome/Chromium**: Primary browser, fully supported
- ✅ **Edge**: Native Windows browser, excellent compatibility
- ✅ **Firefox**: Fully supported alternative
- ❌ **Safari**: Not available on Windows (automatically falls back to Chrome)

**Recommended browsers for Windows 11:**
1. **Chrome** (best compatibility with Roku Channel on Windows)
2. **Edge** (native Windows browser, excellent performance)
3. **Firefox** (reliable alternative)

**Note:** Roku Channel works well with Chrome and Edge on Windows 11, unlike macOS where Chrome may be blocked.

### Debug Mode

Run with debug logging for detailed information:

```bash
python main.py --log-level DEBUG
```

## Framework Choice

This implementation uses **Playwright**, which offers:

- ✅ **Modern and fast** - Built for modern web apps
- ✅ **Multi-browser support** - Safari, Chrome, Firefox, Edge
- ✅ **Built-in browser management** - No driver setup needed
- ✅ **Excellent debugging** - Built-in tracing and debugging tools
- ✅ **Auto-waiting** - Smart waiting for elements and network
- ✅ **Cross-platform** - Works on macOS, Windows, Linux

### Why Playwright over Selenium?

- **Faster execution** - No WebDriver overhead
- **Better reliability** - Built-in auto-waiting and retry logic
- **Modern API** - More intuitive and powerful
- **Better debugging** - Built-in tracing and screenshots
- **Active development** - Microsoft-backed, actively maintained

## Legal Notice

This tool is for educational and testing purposes only. Please ensure you comply with:
- Roku's Terms of Service
- Local laws and regulations
- Platform usage policies

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is for educational purposes. Use responsibly and ethically.
