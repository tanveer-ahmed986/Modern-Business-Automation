"""
LLM Service for MBAS AI Natural Language Queries (Premium Feature)

Uses Phi-3-mini-4k-instruct model for offline natural language processing.
"""

from pathlib import Path
from typing import Optional


class LLMService:
    """
    Manages the local LLM for natural language business queries.

    This service loads the Phi-3 model and provides a query interface
    for Premium tier users to ask questions about their business data.
    """

    def __init__(self):
        """Initialize LLM service and attempt to load model."""
        self.model = None
        self.model_path = self._find_model()

        if self.model_path and self.model_path.exists():
            self._load_model()
        else:
            print("[!] LLM model not found. AI queries will show fallback messages.")
            print(f"    Expected location: {self.model_path}")
            print("    Download with: python scripts/download_model.py")

    def _find_model(self) -> Optional[Path]:
        """
        Locate model file in bundled resources or dev directory.

        Returns:
            Path to model file, or None if not found
        """
        # Try multiple possible locations
        possible_paths = [
            # Production: Tauri resource bundle
            Path("resources/models/Phi-3-mini-4k-instruct.q4.gguf"),
            # Development: Local models directory
            Path("models/Phi-3-mini-4k-instruct.q4.gguf"),
            # Alternative naming
            Path("models/phi-3-mini-4k-instruct.Q4_K_M.gguf"),
            Path("resources/models/phi-3-mini-4k-instruct.Q4_K_M.gguf"),
        ]

        for path in possible_paths:
            if path.exists():
                return path

        # Return first path as default (for error messages)
        return possible_paths[1]

    def _load_model(self):
        """Load the LLM model using llama-cpp-python."""
        try:
            from llama_cpp import Llama

            print(f"[*] Loading LLM model from {self.model_path}...")
            print("    This may take 10-30 seconds...")

            self.model = Llama(
                model_path=str(self.model_path),
                n_ctx=2048,         # Context window (tokens)
                n_threads=4,        # CPU threads to use
                n_gpu_layers=0,     # CPU-only mode (0 = no GPU)
                verbose=False       # Suppress llama.cpp logs
            )

            print(f"[OK] LLM loaded successfully from {self.model_path}")

        except ImportError:
            print("[!] llama-cpp-python not installed. AI queries disabled.")
            print("    Install with: pip install llama-cpp-python")
            self.model = None

        except Exception as e:
            print(f"[X] Failed to load LLM model: {e}")
            self.model = None

    def query(self, prompt: str, max_tokens: int = 150) -> str:
        """
        Process natural language business query.

        Args:
            prompt: User's question or query
            max_tokens: Maximum response length

        Returns:
            AI-generated response or fallback message
        """
        if not self.model:
            return self._fallback_response(prompt)

        # Create business-specific system prompt
        system_prompt = """You are a business assistant for a retail management system.
You help users understand their sales data, inventory, and reports.
Answer questions concisely and professionally.
Keep responses under 100 words unless detailed analysis is requested.
If you don't have specific data, suggest which report or feature to use."""

        # Combine system prompt with user query
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"

        try:
            response = self.model.create_completion(
                prompt=full_prompt,
                max_tokens=max_tokens,
                stop=["User:", "\n\n\n"],  # Stop sequences
                temperature=0.7,           # Creativity (0.0 = deterministic, 1.0 = creative)
                top_p=0.9,                 # Nucleus sampling
                echo=False                 # Don't echo the prompt
            )

            # Extract response text
            response_text = response["choices"][0]["text"].strip()

            # Handle empty responses
            if not response_text:
                return "I apologize, but I couldn't generate a helpful response. Could you rephrase your question?"

            return response_text

        except Exception as e:
            print(f"[ERROR] LLM query failed: {e}")
            return f"I encountered an error processing your query. Please try rephrasing or contact support."

    def _fallback_response(self, prompt: str) -> str:
        """
        Provide helpful fallback responses when model is unavailable.

        Args:
            prompt: User's query

        Returns:
            Context-aware fallback message
        """
        prompt_lower = prompt.lower()

        # Keyword-based responses
        if any(word in prompt_lower for word in ["sales", "revenue", "report"]):
            return ("I can help with sales reports. The AI Assistant requires the Premium package "
                    "with the AI model installed. For now, use the Reports section to view sales data.")

        elif any(word in prompt_lower for word in ["profit", "loss", "p&l", "margin"]):
            return ("Profit & Loss reports are available in the Reports section (Premium feature). "
                    "To get AI-powered insights, ensure the AI model is downloaded.")

        elif any(word in prompt_lower for word in ["inventory", "stock", "product"]):
            return ("For inventory queries, check the Inventory section. Low stock alerts and "
                    "AI-powered stock predictions require Premium with AI model installed.")

        elif any(word in prompt_lower for word in ["forecast", "predict", "future"]):
            return ("Sales forecasting is available under AI Insights (Premium feature). "
                    "Ensure the AI model is installed for predictive analytics.")

        else:
            return ("AI Assistant unavailable. This feature requires:\n"
                    "1. Premium license tier\n"
                    "2. AI model downloaded (run: python scripts/download_model.py)\n"
                    "3. llama-cpp-python installed (pip install llama-cpp-python)\n\n"
                    "In the meantime, use the Reports and Dashboard sections for insights.")

    def is_available(self) -> bool:
        """Check if LLM is loaded and available."""
        return self.model is not None


# Singleton instance
llm_service = LLMService()


if __name__ == "__main__":
    # Test queries
    print("Testing LLM Service...")
    print("=" * 70)

    test_queries = [
        "What are the top selling products this month?",
        "How is my profit margin?",
        "Show me products with low stock",
        "What's the sales forecast for next week?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {llm_service.query(query)}")
        print("-" * 70)
