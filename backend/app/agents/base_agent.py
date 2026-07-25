from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.integrations.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all AI agents"""
    
    def __init__(self, name: str, gemini_client: GeminiClient):
        self.name = name
        self.gemini_client = gemini_client
        self.logger = logger
        self.status = "idle"
        self.last_run = None
        self.execution_time = 0
        self.retry_count = 0
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent with retry logic"""
        start_time = datetime.utcnow()
        self.status = "running"
        self.retry_count = 0
        
        try:
            self.logger.info(f"Agent {self.name} started processing")
            
            # Validate input
            if not input_data:
                raise ValueError("No input data provided")
            
            # Process
            result = await self.process(input_data)
            
            # Ensure result is dict
            if not isinstance(result, dict):
                result = {"data": result}
            
            self.status = "completed"
            self.execution_time = (datetime.utcnow() - start_time).total_seconds()
            self.last_run = datetime.utcnow()
            
            self.logger.info(
                f"Agent {self.name} completed in {self.execution_time:.2f}s"
            )
            
            return {
                "agent": self.name,
                "status": "success",
                "data": result,
                "execution_time": self.execution_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.retry_count += 1
            self.status = "error"
            self.logger.error(f"Agent {self.name} failed (attempt {self.retry_count}): {str(e)}")
            
            if self.retry_count >= 3:
                return {
                    "agent": self.name,
                    "status": "error",
                    "error": str(e),
                    "retry_count": self.retry_count,
                    "timestamp": datetime.utcnow().isoformat()
                }
            raise
    
    def generate_prompt(self, template: str, context: Dict[str, Any]) -> str:
        """Generate prompt from template with context"""
        try:
            # Format template with context
            return template.format(**context)
        except KeyError as e:
            self.logger.error(f"Missing context key: {e}")
            # Try to find and replace missing keys with empty string
            import re
            pattern = r'\{([^}]+)\}'
            missing_keys = re.findall(pattern, template)
            for key in missing_keys:
                if key not in context:
                    context[key] = ""
            return template.format(**context)
    
    def validate_output(self, output: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate agent output has required fields"""
        missing_fields = [field for field in required_fields if field not in output]
        if missing_fields:
            self.logger.warning(f"Missing fields in output: {missing_fields}")
            return False
        return True
