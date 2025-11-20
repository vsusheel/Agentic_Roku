"""
Roku Movie Automation Agent
Automates playing movies on Roku channel web interface using Playwright
"""
import time
import logging
import os
import platform
from typing import Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, TimeoutError as PlaywrightTimeoutError
from config import AutomationConfig

class RokuMovieAgent:
    """Agent for automating Roku movie playback"""
    
    def __init__(self, config: AutomationConfig):
        self.config = config
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.setup_logging()
        self.setup_screenshots_dir()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('roku_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_screenshots_dir(self):
        """Create screenshots directory if it doesn't exist"""
        if self.config.save_screenshots:
            os.makedirs(self.config.screenshot_dir, exist_ok=True)
            
    def setup_browser(self):
        """Setup and configure the browser using Playwright with cross-platform compatibility (macOS Monterey 12.7.3 and Windows 11)"""
        try:
            self.playwright = sync_playwright().start()
            
            # Detect operating system
            system = platform.system()
            is_windows = system == 'Windows'
            is_macos = system == 'Darwin'
            
            # Browser-specific user agents based on OS
            if is_windows:
                # Windows 11 user agents
                user_agents = {
                    'chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'firefox': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                    'edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                    'safari': None  # Safari not available on Windows
                }
                default_browser = 'chrome'
            elif is_macos:
                # macOS Monterey 12.7.3 user agents
                user_agents = {
                    'safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.6 Safari/605.1.15',
                    'chrome': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'firefox': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.7; rv:121.0) Gecko/20100101 Firefox/121.0',
                    'edge': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
                }
                default_browser = 'safari'
            else:
                # Linux or other OS - use generic user agents
                user_agents = {
                    'chrome': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'firefox': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
                    'edge': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                    'safari': None
                }
                default_browser = 'chrome'
            
            browser_type = self.config.browser.lower()
            
            # Handle Safari on non-macOS systems
            if browser_type == 'safari' and not is_macos:
                self.logger.warning(f"Safari is not available on {system}. Falling back to {default_browser}.")
                browser_type = default_browser
            
            # Launch browser based on configuration with cross-platform compatibility
            if browser_type == 'safari':
                if not is_macos:
                    raise ValueError("Safari is only available on macOS")
                try:
                    self.browser = self.playwright.webkit.launch(
                        headless=self.config.headless,
                        slow_mo=self.config.slow_mo
                    )
                    self.logger.info("Safari (WebKit) launched successfully")
                except Exception as safari_error:
                    self.logger.warning(f"Safari launch failed: {safari_error}")
                    self.logger.info("Falling back to Firefox")
                    browser_type = 'firefox'
                    self.browser = self.playwright.firefox.launch(
                        headless=self.config.headless,
                        slow_mo=self.config.slow_mo
                    )
            elif browser_type == 'chrome' or browser_type == 'chromium':
                self.browser = self.playwright.chromium.launch(
                    headless=self.config.headless,
                    slow_mo=self.config.slow_mo,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-features=IsolateOrigins,site-per-process',
                        '--disable-site-isolation-trials'
                    ]
                )
            elif browser_type == 'firefox':
                self.browser = self.playwright.firefox.launch(
                    headless=self.config.headless,
                    slow_mo=self.config.slow_mo
                )
            elif browser_type == 'edge':
                self.browser = self.playwright.chromium.launch(
                    headless=self.config.headless,
                    slow_mo=self.config.slow_mo,
                    channel='msedge',
                    args=[
                        '--disable-blink-features=AutomationControlled'
                    ]
                )
            else:
                raise ValueError(f"Unsupported browser: {self.config.browser}")
            
            # Create browser context with cross-platform compatible settings
            # Select appropriate timezone based on OS
            timezone = 'America/Los_Angeles' if is_macos or is_windows else 'UTC'
            
            # Get user agent with safe fallback
            user_agent = user_agents.get(browser_type)
            if not user_agent:
                user_agent = user_agents.get(default_browser)
            if not user_agent:
                user_agent = user_agents.get('firefox') or user_agents.get('chrome')
            
            context_options = {
                'viewport': {'width': self.config.window_size[0], 'height': self.config.window_size[1]},
                'user_agent': user_agent,
                'locale': 'en-US',
                'timezone_id': timezone,
                # Extra HTTP headers for compatibility
                'extra_http_headers': {
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                }
            }
            
            self.context = self.browser.new_context(**context_options)
            
            # Grant permissions for autoplay (important for video playback)
            try:
                base_url = self.config.movie_url.split('/details')[0]
                self.context.grant_permissions(['autoplay'], origin=base_url)
                self.logger.debug(f"Granted autoplay permissions for {base_url}")
            except Exception as perm_error:
                self.logger.warning(f"Could not grant permissions: {perm_error}")
            
            # Create new page
            self.page = self.context.new_page()
            self.page.set_default_timeout(self.config.page_load_timeout * 1000)  # Playwright uses milliseconds
            
            os_name = "Windows 11" if is_windows else ("macOS Monterey" if is_macos else system)
            self.logger.info(f"Successfully initialized {browser_type} browser with Playwright on {os_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup browser: {e}")
            self.logger.error(f"Browser: {self.config.browser}, Error type: {type(e).__name__}")
            
            # Try Firefox as fallback
            if self.config.browser.lower() != 'firefox':
                self.logger.info("Attempting fallback to Firefox...")
                try:
                    self.browser = self.playwright.firefox.launch(
                        headless=self.config.headless,
                        slow_mo=self.config.slow_mo
                    )
                    # Get appropriate user agent for fallback
                    fallback_ua = user_agents.get('firefox') or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
                    self.context = self.browser.new_context(
                        viewport={'width': self.config.window_size[0], 'height': self.config.window_size[1]},
                        user_agent=fallback_ua
                    )
                    self.page = self.context.new_page()
                    self.page.set_default_timeout(self.config.page_load_timeout * 1000)
                    self.logger.info("Successfully initialized Firefox as fallback browser")
                except Exception as fallback_error:
                    self.logger.error(f"Firefox fallback also failed: {fallback_error}")
                    raise
            else:
                raise
            
    def take_screenshot(self, name: str):
        """Take a screenshot for debugging"""
        if self.config.save_screenshots and self.page:
            timestamp = int(time.time())
            filename = f"{self.config.screenshot_dir}/{name}_{timestamp}.png"
            self.page.screenshot(path=filename)
            self.logger.info(f"Screenshot saved: {filename}")
            
    def wait_for_element(self, selector: str, timeout: int = None) -> bool:
        """Wait for an element to be present and clickable"""
        timeout_ms = (timeout or self.config.element_wait_timeout) * 1000  # Convert to milliseconds
        try:
            self.page.wait_for_selector(selector, timeout=timeout_ms, state='visible')
            return True
        except PlaywrightTimeoutError:
            self.logger.warning(f"Element not found: {selector}")
            return False
            
    def find_play_button(self) -> bool:
        """Find and click the play button"""
        try:
            # Try multiple selectors for play button, including Roku-specific ones
            selectors = [
                # Roku-specific selectors
                "a.roku-button.icon-play",
                "a[aria-label*='Play Ice Cross']",
                "a[href*='/watch/']",
                ".roku-button.padded.icon-play",
                # Generic selectors
                self.config.play_button_selector,
                "button[aria-label*='play']",
                "button[aria-label*='Play']",
                ".play-button",
                "[data-testid*='play']",
                "button:has-text('Play')",
                "button:has-text('play')",
                "a:has-text('Play')"
            ]
            
            for selector in selectors:
                try:
                    if self.wait_for_element(selector, 5):
                        # Get the element and try different click methods
                        element = self.page.locator(selector)
                        
                        # Try regular click first
                        try:
                            element.click()
                            self.logger.info(f"Successfully clicked play button with selector: {selector}")
                            return True
                        except Exception as click_error:
                            self.logger.debug(f"Regular click failed for {selector}: {click_error}")
                            
                            # Try force click
                            try:
                                element.click(force=True)
                                self.logger.info(f"Successfully force-clicked play button with selector: {selector}")
                                return True
                            except Exception as force_error:
                                self.logger.debug(f"Force click failed for {selector}: {force_error}")
                                
                                # Try JavaScript click
                                try:
                                    element.evaluate("element => element.click()")
                                    self.logger.info(f"Successfully JS-clicked play button with selector: {selector}")
                                    return True
                                except Exception as js_error:
                                    self.logger.debug(f"JS click failed for {selector}: {js_error}")
                                    continue
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            self.logger.error("Could not find play button with any selector")
            return False
            
        except Exception as e:
            self.logger.error(f"Error finding play button: {e}")
            return False
            
    def is_movie_playing(self) -> bool:
        """Check if the movie is currently playing"""
        try:
            # First check if we're on the watch page
            current_url = self.page.url
            if "/watch/" in current_url:
                self.logger.info("On watch page, checking for video elements...")
                
                # Look for pause button or video controls
                pause_selectors = [
                    self.config.pause_button_selector,
                    "button[aria-label*='pause']",
                    "button[aria-label*='Pause']",
                    ".pause-button",
                    "[data-testid*='pause']",
                    # Roku-specific selectors
                    ".roku-button.icon-pause",
                    "a[aria-label*='Pause']",
                    ".roku-button[aria-label*='pause']"
                ]
                
                for selector in pause_selectors:
                    try:
                        if self.page.locator(selector).is_visible():
                            self.logger.info(f"Found pause button with selector: {selector}")
                            return True
                    except:
                        continue
                
                # Check for video element or player (more comprehensive)
                video_selectors = [
                    "video",
                    ".video-player",
                    ".player",
                    "[data-testid*='video']",
                    ".roku-video-player",
                    # Additional selectors for embedded players
                    "iframe[src*='player']",
                    "iframe[src*='video']",
                    ".embed-player",
                    ".media-player",
                    "[class*='player']",
                    "[class*='video']",
                    # Roku-specific video containers
                    ".roku-player",
                    ".roku-video-container",
                    ".video-container"
                ]
                
                for selector in video_selectors:
                    try:
                        if self.page.locator(selector).is_visible():
                            self.logger.info(f"Found video element with selector: {selector}")
                            return True
                    except:
                        continue
                
                # Check for video controls or progress bars
                control_selectors = [
                    ".progress-bar",
                    ".seek-bar",
                    ".time-display",
                    "[class*='progress']",
                    "[class*='seek']",
                    ".video-controls",
                    ".player-controls",
                    # Roku-specific controls
                    ".roku-controls",
                    ".roku-progress-bar",
                    ".roku-time-display"
                ]
                
                for selector in control_selectors:
                    try:
                        if self.page.locator(selector).is_visible():
                            self.logger.info(f"Found video controls with selector: {selector}")
                            return True
                    except:
                        continue
                
                # Check for any modal or overlay that might contain the video
                modal_selectors = [
                    ".modal",
                    ".overlay",
                    ".popup",
                    "[class*='modal']",
                    "[class*='overlay']",
                    ".video-modal",
                    ".player-modal",
                    ".roku-modal"
                ]
                
                for selector in modal_selectors:
                    try:
                        if self.page.locator(selector).is_visible():
                            self.logger.info(f"Found modal/overlay with selector: {selector}")
                            # Check if this modal contains video elements
                            modal = self.page.locator(selector)
                            if modal.locator("video").count() > 0 or modal.locator("iframe").count() > 0:
                                self.logger.info("Modal contains video elements")
                                return True
                    except:
                        continue
                
                # If we're on watch page but no video elements found, 
                # check if there's a loading indicator
                loading_selectors = [
                    ".loading",
                    ".spinner",
                    "[class*='loading']",
                    "[class*='spinner']",
                    ".roku-loading"
                ]
                
                for selector in loading_selectors:
                    try:
                        if self.page.locator(selector).is_visible():
                            self.logger.info(f"Found loading indicator: {selector}")
                            return True  # Assume video is loading/playing
                    except:
                        continue
                
                # If we're on watch page and no specific elements found,
                # assume video is playing (Roku might use custom video implementation)
                self.logger.info("On watch page with no specific video elements detected, assuming video is playing")
                return True
            
            # If not on watch page, video is definitely not playing
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking if movie is playing: {e}")
            return False
            
    def analyze_page_structure(self):
        """Analyze the page structure to find video elements"""
        try:
            self.logger.info("=== PAGE STRUCTURE ANALYSIS ===")
            
            # Check for video elements
            video_count = self.page.locator("video").count()
            self.logger.info(f"Video elements found: {video_count}")
            
            # Check for iframes
            iframe_count = self.page.locator("iframe").count()
            self.logger.info(f"IFrame elements found: {iframe_count}")
            
            # Check for common video player classes
            player_classes = [
                "video-player", "player", "media-player", "embed-player",
                "roku-video-player", "video-container", "player-container"
            ]
            
            for class_name in player_classes:
                count = self.page.locator(f".{class_name}").count()
                if count > 0:
                    self.logger.info(f"Found {count} elements with class '{class_name}'")
            
            # Check for modals and overlays
            modal_count = self.page.locator(".modal, .overlay, .popup").count()
            self.logger.info(f"Modal/overlay elements found: {modal_count}")
            
            # Check for any elements with 'video' or 'player' in class names
            video_elements = self.page.locator("[class*='video'], [class*='player']").count()
            self.logger.info(f"Elements with 'video' or 'player' in class: {video_elements}")
            
            # Check for any elements with 'play' or 'pause' in class names
            control_elements = self.page.locator("[class*='play'], [class*='pause']").count()
            self.logger.info(f"Elements with 'play' or 'pause' in class: {control_elements}")
            
            # Check page title
            title = self.page.title()
            self.logger.info(f"Page title: {title}")
            
            # Check for any JavaScript errors or console messages
            # (This would require additional setup in Playwright)
            
            self.logger.info("=== END PAGE ANALYSIS ===")
            
        except Exception as e:
            self.logger.error(f"Error analyzing page structure: {e}")

    def wait_for_movie_completion(self):
        """Wait for the movie to finish playing"""
        self.logger.info("Waiting for movie to complete...")
        start_time = time.time()
        
        while True:
            if not self.is_movie_playing():
                self.logger.info("Movie appears to have finished")
                break
                
            # Check if we've been waiting too long (safety timeout)
            if time.time() - start_time > 3600:  # 1 hour timeout
                self.logger.warning("Movie timeout reached, assuming completion")
                break
                
            time.sleep(10)  # Check every 10 seconds
            
    def handle_modal_overlay(self) -> bool:
        """Handle any modal overlays that might block interaction"""
        try:
            # Check if there's a visible modal overlay present (not hidden)
            modal_overlay = self.page.locator(".roku-modal-overlay:not(.hidden)")
            if modal_overlay.count() == 0 or not modal_overlay.first.is_visible():
                return False
                
            self.logger.info("Modal overlay detected, attempting to dismiss...")
            
            # Look for common modal close buttons
            modal_selectors = [
                # Specific to anonymous-nudge modal
                ".roku-modal-overlay.anonymous-nudge .close",
                ".roku-modal-overlay.anonymous-nudge button[aria-label*='close']",
                ".roku-modal-overlay.anonymous-nudge button[aria-label*='Close']",
                ".roku-modal-overlay.anonymous-nudge .close-button",
                ".roku-modal-overlay.anonymous-nudge button[data-testid*='close']",
                ".roku-modal-overlay.anonymous-nudge .modal-close",
                # Look for X button or close symbol
                ".roku-modal-overlay.anonymous-nudge [aria-label='Close']",
                ".roku-modal-overlay.anonymous-nudge [aria-label='close']",
                ".roku-modal-overlay.anonymous-nudge button:has-text('×')",
                ".roku-modal-overlay.anonymous-nudge button:has-text('✕')",
                # Generic modal close buttons
                ".roku-modal-overlay .close",
                ".roku-modal-overlay button[aria-label*='close']",
                ".roku-modal-overlay button[aria-label*='Close']",
                ".roku-modal-overlay .close-button",
                ".roku-modal-overlay button[data-testid*='close']",
                ".roku-modal-overlay .modal-close",
                # Roku-specific selectors
                ".roku-modal-overlay .roku-button[aria-label*='close']",
                ".roku-modal-overlay .roku-button[aria-label*='Close']",
                # Generic close buttons
                ".roku-modal-overlay button:has-text('Close')",
                ".roku-modal-overlay button:has-text('close')",
                ".roku-modal-overlay [role='button']:has-text('Close')",
                ".roku-modal-overlay [role='button']:has-text('close')"
            ]
            
            for selector in modal_selectors:
                try:
                    close_button = self.page.locator(selector)
                    if close_button.is_visible():
                        close_button.click()
                        self.logger.info(f"Closed modal with selector: {selector}")
                        time.sleep(2)  # Wait for modal to close
                        return True
                except Exception as e:
                    self.logger.debug(f"Close button {selector} failed: {e}")
                    continue
            
            # Try pressing Escape key
            try:
                self.page.keyboard.press("Escape")
                self.logger.info("Pressed Escape key to dismiss modal")
                time.sleep(2)
                if modal_overlay.count() == 0 or not modal_overlay.first.is_visible():
                    return True
            except Exception as e:
                self.logger.debug(f"Escape key failed: {e}")
            
            # If no close button found, try clicking outside the modal
            try:
                # Click on the page background to dismiss modal
                self.page.click("body", position={"x": 10, "y": 10})
                self.logger.info("Clicked outside modal to dismiss")
                time.sleep(2)
                if modal_overlay.count() == 0 or not modal_overlay.first.is_visible():
                    return True
            except Exception as e:
                self.logger.debug(f"Click outside modal failed: {e}")
            
            # Try clicking on the modal overlay itself (sometimes this dismisses it)
            try:
                modal_overlay.first.click()
                self.logger.info("Clicked on modal overlay to dismiss")
                time.sleep(2)
                if modal_overlay.count() == 0 or not modal_overlay.first.is_visible():
                    return True
            except Exception as e:
                self.logger.debug(f"Click on modal overlay failed: {e}")
                
            self.logger.warning("Could not dismiss modal overlay")
            return False
            
        except Exception as e:
            self.logger.warning(f"Error handling modal overlay: {e}")
            return False

    def play_movie(self) -> bool:
        """Play the movie once"""
        try:
            self.logger.info(f"Navigating to: {self.config.movie_url}")
            self.page.goto(self.config.movie_url)
            self.take_screenshot("page_loaded")
            
            # Wait for page to load
            time.sleep(3)
            
            # Handle any modal overlays first
            modal_dismissed = self.handle_modal_overlay()
            if modal_dismissed:
                self.logger.info("Modal overlay dismissed, waiting for page to stabilize...")
                time.sleep(2)
            
            # Try to find and click play button
            if not self.find_play_button():
                self.logger.error("Failed to start movie playback")
                return False
                
            self.take_screenshot("play_clicked")
            
            # Wait for potential navigation to video player
            try:
                # Wait for navigation with a timeout
                self.page.wait_for_url("**/watch/**", timeout=10000)
                self.logger.info("Successfully navigated to video player page")
            except PlaywrightTimeoutError:
                self.logger.info("No navigation detected, continuing with current page")
            
            # Wait a moment for playback to start
            time.sleep(3)
            
            # Debug: Check current URL and page state
            current_url = self.page.url
            self.logger.info(f"Current URL after play click: {current_url}")
            
            # Take another screenshot to see the state
            self.take_screenshot("after_play_click")
            
            # Debug: Analyze page structure for video elements
            self.analyze_page_structure()
            
            if self.is_movie_playing():
                self.logger.info("Movie is now playing")
                self.wait_for_movie_completion()
                return True
            else:
                self.logger.error("Movie did not start playing")
                # Let's wait a bit longer and try again
                time.sleep(5)
                if self.is_movie_playing():
                    self.logger.info("Movie started playing after additional wait")
                    self.wait_for_movie_completion()
                    return True
                else:
                    self.logger.error("Movie still not playing after extended wait")
                    return False
                
        except Exception as e:
            self.logger.error(f"Error playing movie: {e}")
            return False
            
    def run_automation(self):
        """Run the complete automation with looping"""
        try:
            self.setup_browser()
            self.logger.info("Starting Roku movie automation")
            
            loop_count = 0
            
            while True:
                loop_count += 1
                self.logger.info(f"Starting loop {loop_count}")
                
                success = self.play_movie()
                
                if success:
                    self.logger.info(f"Loop {loop_count} completed successfully")
                else:
                    self.logger.error(f"Loop {loop_count} failed")
                
                # Check if we should continue looping
                if self.config.max_loops > 0 and loop_count >= self.config.max_loops:
                    self.logger.info(f"Reached maximum loops ({self.config.max_loops})")
                    break
                    
                # Wait before next loop
                if self.config.max_loops == -1 or loop_count < self.config.max_loops:
                    self.logger.info(f"Waiting {self.config.loop_delay} seconds before next loop...")
                    time.sleep(self.config.loop_delay)
                    
        except KeyboardInterrupt:
            self.logger.info("Automation interrupted by user")
        except Exception as e:
            self.logger.error(f"Automation failed: {e}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self.logger.info("Browser resources cleaned up")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
