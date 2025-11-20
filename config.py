"""
Configuration settings for Roku Movie Automation
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AutomationConfig:
    """Configuration class for automation settings"""
    
    # Target URL
    movie_url: str = "https://therokuchannel.roku.com/details/3fddf29ad3490e7117d0b599b608b674/ice-cross-life-on-the-edge"
    
    # Browser settings
    browser: str = "safari"  # safari, chrome, firefox, edge
    headless: bool = False
    window_size: tuple = (1920, 1080)
    slow_mo: int = 0  # Slow down operations by specified ms
    
    # Automation settings
    max_loops: int = 5  # Set to -1 for infinite loops
    loop_delay: int = 5  # Seconds to wait between loops
    page_load_timeout: int = 30
    element_wait_timeout: int = 10
    
    # Playback settings
    play_button_selector: str = "button[data-testid='play-button'], .play-button, [aria-label*='play'], [aria-label*='Play']"
    pause_button_selector: str = "button[data-testid='pause-button'], .pause-button, [aria-label*='pause'], [aria-label*='Pause']"
    
    # Logging
    log_level: str = "INFO"
    save_screenshots: bool = True
    screenshot_dir: str = "screenshots"
    
    @classmethod
    def from_env(cls) -> 'AutomationConfig':
        """Load configuration from environment variables"""
        return cls(
            movie_url=os.getenv('MOVIE_URL', cls.movie_url),
            browser=os.getenv('BROWSER', cls.browser),
            headless=os.getenv('HEADLESS', 'false').lower() == 'true',
            slow_mo=int(os.getenv('SLOW_MO', cls.slow_mo)),
            max_loops=int(os.getenv('MAX_LOOPS', cls.max_loops)),
            loop_delay=int(os.getenv('LOOP_DELAY', cls.loop_delay)),
            log_level=os.getenv('LOG_LEVEL', cls.log_level)
        )
