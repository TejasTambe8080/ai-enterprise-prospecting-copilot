import google.generativeai as genai
from typing import Dict, Any, Optional, AsyncIterator
import json
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config.settings import settings

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for Google Gemini API with retry logic and error handling"""
    
    def __init__(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            self.embedding_model = settings.GEMINI_EMBEDDING_MODEL
            self.logger = logger
            self.semaphore = asyncio.Semaphore(5)  # Rate limit
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate_text(self, prompt: str) -> str:
        """Generate text response from Gemini"""
        async with self.semaphore:
            try:
                response = await self.model.generate_content_async(prompt)
                return response.text
            except Exception as e:
                self.logger.error(f"Gemini API error: {str(e)}")
                raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Generate JSON response from Gemini"""
        async with self.semaphore:
            try:
                # Add instruction to return valid JSON
                json_prompt = f"{prompt}\n\nReturn ONLY valid JSON, no additional text."
                
                response = await self.model.generate_content_async(json_prompt)
                text = response.text
                
                # Clean the response
                text = text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.startswith('```'):
                    text = text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                text = text.strip()
                
                # Parse JSON
                return json.loads(text)
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {str(e)}")
                self.logger.error(f"Response text: {text[:200]}")
                # Try to extract JSON from response
                try:
                    import re
                    json_match = re.search(r'\{.*\}', text, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass
                return {"error": "Invalid JSON response", "raw": text[:500]}
            except Exception as e:
                self.logger.error(f"Gemini API error: {str(e)}")
                raise
    
    async def generate_embeddings(self, text: str) -> list:
        """Generate embeddings for text"""
        async with self.semaphore:
            try:
                result = await genai.embed_content_async(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                return result["embedding"]
            except Exception as e:
                self.logger.error(f"Embedding generation error: {str(e)}")
                raise
    
    async def stream_response(self, prompt: str) -> AsyncIterator[str]:
        """Stream response from Gemini"""
        async with self.semaphore:
            try:
                response = await self.model.generate_content_async(prompt, stream=True)
                async for chunk in response:
                    yield chunk.text
            except Exception as e:
                self.logger.error(f"Gemini streaming error: {str(e)}")
                raise