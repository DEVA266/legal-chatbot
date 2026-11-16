import os

# Application Info
APP_TITLE = "LexCraft AI - Legal Document Drafting Assistant"
APP_SUBTITLE = "Specialized AI drafting for Indian Legal Practice (Section 138 NI Act, NDA, Commercial Notices)"

# Model Pricing per 1,000,000 tokens (USD) for estimating costs
MODEL_PRICING = {
    # Gemini Models (Very fast & affordable / free tier available)
    "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
    "gemini-3.8-flash": {"input": 0.075, "output": 0.30},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    # OpenAI Models
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    # Groq Models
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    # Mock / Demo Engine (Free)
    "mock-offline-engine": {"input": 0.00, "output": 0.00},
}

USD_TO_INR = 86.50

SUPPORTED_DOCUMENTS = [
    {
        "id": "sec_138",
        "title": "Section 138 NI Act (Cheque Dishonour Notice)",
        "law": "Negotiable Instruments Act, 1881",
        "badge": "Criminal / Banking",
        "description": "Statutory demand notice under Section 138 with 15-day cure period and Section 141 corporate liability."
    },
    {
        "id": "nda",
        "title": "Non-Disclosure Agreement (NDA)",
        "law": "Indian Contract Act, 1872",
        "badge": "Corporate / Commercial",
        "description": "Comprehensive Mutual or Unilateral NDA with trade secret protection, non-solicitation, and arbitration."
    },
    {
        "id": "recovery_notice",
        "title": "Legal Notice for Recovery of Dues",
        "law": "Commercial Law / CPC Order 37",
        "badge": "Civil / Commercial",
        "description": "Formal advocate demand notice for unpaid business invoices with 18% interest and insolvency warning."
    }
]
