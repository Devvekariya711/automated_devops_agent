import sys
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 1. Load environment variables (API Key)
load_dotenv()
logger.info("Environment variables loaded")

# 2. Add current directory to Python path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        logger.info("Starting DevOps Agent Web Server...")
        
        # Import the ADK web server CLI
        from google.adk.cli import adk_web_server as web
        
        print("Starting DevOps Agent Web Server...")
        print("Point your browser to the URL shown below (usually http://localhost:3000 or 8080)")
        
        # 3. Mimic the CLI command: "adk devops_automator.agent:root_agent"
        # This tells the server where to find the 'root_agent' object
        sys.argv = ["adk", "devops_automator.agent:root_agent"]
        
        # 4. Run the server
        web()
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print("Error: Could not import google-adk.")
        print("Please ensure you ran: pip install -r requirements.txt")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"An error occurred: {e}")