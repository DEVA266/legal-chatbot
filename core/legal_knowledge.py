"""
Legal knowledge base containing statutory checklists, validation rules,
and legal standard references for Indian Legal Practice.
"""

LEGAL_CHECKLISTS = {
    "sec_138": {
        "title": "Section 138 Negotiable Instruments Act, 1881",
        "jurisdiction": "India",
        "governing_statutes": [
            "Section 138 (Dishonour of cheque for insufficiency, etc., of funds)",
            "Section 139 (Presumption in favour of holder in due course)",
            "Section 141 (Offences by companies and vicarious liability of Directors)",
            "Section 142 (Cognizance of offences and 1-month court limitation period)"
        ],
        "mandatory_fields": [
            ("complainant_name", "Complainant / Payee Name & Address"),
            ("accused_name", "Accused / Drawer Name, Designation & Address"),
            ("debt_consideration", "Transaction / Consideration for which cheque was issued"),
            ("cheque_number", "Cheque Number"),
            ("cheque_date", "Date on the Cheque"),
            ("cheque_amount", "Cheque Amount (in Rs.)"),
            ("drawee_bank", "Drawee Bank Name & Branch (Accused's bank)"),
            ("presentation_date", "Date of presentation in Payee's Bank"),
            ("memo_date", "Date of Cheque Return Memo from the bank"),
            ("dishonour_reason", "Exact Bank Return Memo Reason (e.g. Funds Insufficient, Account Closed)")
        ],
        "statutory_rules": [
            "Cheque must be presented within validity (3 months from cheque date).",
            "Statutory notice must be dispatched within 30 days of receiving the bank dishonour memo.",
            "Demand notice must grant 15 clear days from receipt to pay the amount.",
            "If drawer fails to pay within 15 days, cause of action arises on day 16; Complaint must be filed within 30 days thereafter before the Judicial Magistrate."
        ]
    },
    "nda": {
        "title": "Non-Disclosure Agreement (NDA)",
        "jurisdiction": "India (Indian Contract Act, 1872)",
        "governing_statutes": [
            "Indian Contract Act, 1872 (Section 27 - restrictive covenants, Section 73 - damages)",
            "Specific Relief Act, 1963 (Section 38 - Injunctions)",
            "Arbitration and Conciliation Act, 1996"
        ],
        "mandatory_fields": [
            ("type", "Type of NDA (Mutual / Bilateral or Unilateral / One-way)"),
            ("disclosing_party", "Disclosing Party Name, Address & Signatory"),
            ("receiving_party", "Receiving Party Name, Address & Signatory"),
            ("purpose", "Specific Permitted Purpose of disclosure"),
            ("term_years", "Duration of agreement (e.g. 2 years)"),
            ("survival_years", "Confidentiality survival period post-termination (e.g. 3 years or perpetual for trade secrets)"),
            ("governing_city", "Exclusive Court Jurisdiction & Arbitration Seat (e.g. Mumbai, Delhi, Bengaluru)")
        ],
        "statutory_rules": [
            "Standard exclusions (prior knowledge, public domain, independent development) must be included.",
            "Remedies must include equitable injunctive relief without proof of actual monetary loss.",
            "Restraint of trade covenants must be reasonable under Section 27 of Indian Contract Act."
        ]
    },
    "recovery_notice": {
        "title": "Legal Notice for Recovery of Dues & Breach of Contract",
        "jurisdiction": "India",
        "governing_statutes": [
            "Indian Contract Act, 1872 (Section 73 - Compensation for breach)",
            "Code of Civil Procedure, 1908 (Order XXXVII - Summary Suit)",
            "Commercial Courts Act, 2015",
            "Insolvency and Bankruptcy Code, 2016 (Section 8 Demand Notice, where applicable)"
        ],
        "mandatory_fields": [
            ("creditor_name", "Creditor / Client Name & Address"),
            ("debtor_name", "Debtor / Defaulter Name & Address"),
            ("transaction_type", "Nature of business / services / contract"),
            ("invoices", "Invoice Numbers, Dates and Individual Amounts"),
            ("principal_due", "Total Principal Amount Outstanding"),
            ("interest_rate", "Claimed Interest Rate (e.g. 18% or 24% p.a.)"),
            ("cure_period", "Time given to pay (normally 15 days)")
        ],
        "statutory_rules": [
            "Interest must be supported by contract terms or statutory interest under MSMED Act (if registered MSME) or Interest Act, 1978.",
            "Must state warning of Civil Summary Suit (Order 37 CPC) and criminal prosecution under IPC/BNS for cheating if dishonest inducement existed."
        ]
    }
}
