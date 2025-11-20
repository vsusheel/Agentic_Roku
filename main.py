#!/usr/bin/env python3
"""
Main entry point for Roku Movie Automation
"""
import argparse
import sys
from config import AutomationConfig
from roku_automation import RokuMovieAgent

def main():
    """Main function to run the automation"""
    parser = argparse.ArgumentParser(description='Roku Movie Automation Agent')
    parser.add_argument('--max-loops', type=int, default=5, 
                       help='Maximum number of loops (-1 for infinite)')
    parser.add_argument('--loop-delay', type=int, default=5,
                       help='Delay between loops in seconds')
    parser.add_argument('--browser', choices=['safari', 'chrome', 'firefox', 'edge'], 
                       default='safari', help='Browser to use')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--slow-mo', type=int, default=0,
                       help='Slow down operations by specified milliseconds')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level')
    parser.add_argument('--config-file', type=str,
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Create configuration
    config = AutomationConfig(
        max_loops=args.max_loops,
        loop_delay=args.loop_delay,
        browser=args.browser,
        headless=args.headless,
        slow_mo=args.slow_mo,
        log_level=args.log_level
    )
    
    # Create and run agent
    agent = RokuMovieAgent(config)
    
    try:
        agent.run_automation()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
