# LexCraft AI - Legal Document Drafting Assistant & Intake Bot

Specialized AI-powered legal document drafting application designed for Indian legal professionals.

## 🚀 Key Features

1. **Intelligent Intake Interview Bot**:
   - Detects the legal document from informal prompts like *"Draft me a document on section 138"*.
   - Automatically asks relevant statutory questions (Parties, Cheque numbers, Return memo date, Dishonour reason) without overwhelming the lawyer.
2. **Nails Down 3 Core Practice Documents**:
   - **Section 138 Negotiable Instruments Act, 1881**: Statutory demand notice with 15-day cure period and Section 141 corporate director liability.
   - **Non-Disclosure Agreement (NDA)**: Comprehensive Mutual / Unilateral NDA under Indian Contract Act, 1872.
   - **Commercial Recovery Notice**: Legal demand notice under Order 37 CPC and Commercial Courts Act for unpaid invoices.
3. **Live Split-Screen Dual Interface**:
   - **Left Panel**: Lawyer Chat & Intake Questionnaire.
   - **Right Panel**: Real-time Document Preview with 1-click **Download as Word (.docx)** and **Markdown (.md)**.
4. **Iterative Refinement & Editing**:
   - The lawyer can ask for edits like *"Add Section 141 Director Liability"*, *"Change interest rate to 24% p.a."*, or *"Change jurisdiction to Mumbai courts"*, and the live draft updates instantly.
5. **Real-Time Token Usage & Cost Telemetry**:
   - Tracks **Input (Prompt) Tokens**, **Output (Completion) Tokens**, and **Total Tokens** on every single turn.
   - Displays a token badge under every message.
   - Persistent sidebar dashboard showing cumulative session tokens and estimated cost in both **$ USD** and **₹ INR**.
6. **Ultra-Lightweight on Hardware**:
   - Consumes only ~150MB of RAM.
   - Runs easily on any PC (Ryzen 5500, 16GB RAM) and can be accessed directly from your mobile phone!

---

## 🛠️ Quick Start

### 1. Run the App
Open your terminal in this directory and execute:

```powershell
python -m streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### 2. Mobile Testing (On your phone)
1. Ensure your phone is connected to the same Wi-Fi network as this PC.
2. Open your mobile browser (Chrome/Safari) and navigate to:
   ```
   http://192.168.1.6:8501
   ```
*(Replace with your current local IP if your Wi-Fi assigns a different address).*

### 3. API Key Setup (Optional)
- **Offline Demo Mode**: Works completely offline out of the box with realistic legal simulations and token calculations even if no API key is provided!
- **Live AI Models**: Simply paste your Google Gemini API key (free at [Google AI Studio](https://aistudio.google.com/)) or OpenAI key in the sidebar input box or in a `.env` file.

---

## 📂 Project Structure

```
Legal ChatBot/
├── app.py                      # Main Streamlit Dual-Pane Application
├── config.py                   # Model constants, token pricing, document metadata
├── core/
│   ├── docx_exporter.py        # Professional Word (.docx) generator with court styling
│   ├── legal_knowledge.py      # Indian statutory checklists & compliance rules
│   ├── llm_engine.py           # Unified LLM caller (Gemini, OpenAI, Mock) + Token Tracker
│   └── prompts.py              # Master Legal Associate System Prompt
├── templates/                  # Reference legal templates
│   ├── mutual_nda.md           # Standard Indian NDA
│   ├── recovery_notice.md      # Commercial Recovery Notice (Order 37 CPC)
│   └── section_138_notice.md   # Section 138 NI Act Statutory Notice
├── .env.example
└── README.md
```
