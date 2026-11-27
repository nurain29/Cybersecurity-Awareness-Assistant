
"""
Automated sample-question check script for CyberSafe Assistant.

Run offline (retrieval check):
    python tests/check_sample_questions.py

Run live (with Gemini API key):
    python tests/check_sample_questions.py --live
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.retrieval import retrieve_context


SAMPLE_CHECKS = [
    (
        "Phishing (EN)",
        "I received an email from my bank asking me to verify my account via a link. Is it safe?",
        ["phishing", "link"]
    ),
    (
        "Weak Password (BM/Manglish)",
        "Password saya 12345678, selamat tak?",
        ["password", "strong"]
    ),
    (
        "MFA / OTP (EN)",
        "Why do I need an OTP when I already have a password?",
        ["multi-factor", "mfa", "otp", "authentication"]
    ),
    (
        "Malware (BM)",
        "Apa itu malware?",
        ["malware", "software", "virus"]
    ),
    (
        "Public Wi-Fi (EN)",
        "Can I use free mall Wi-Fi for online banking?",
        ["wi-fi", "public", "network"]
    ),
    (
        "Privacy / IC (EN)",
        "Someone online asked for a photo of my identity card. Should I send it?",
        ["identity", "personal", "verify"]
    ),
    (
        "Software Updates (EN)",
        "Can I ignore phone software updates?",
        ["update", "security"]
    ),
    (
        "Social Engineering (EN)",
        "My boss urgently WhatsApped asking for a money transfer. What should I do?",
        ["verify", "urgent", "scam", "social"]
    ),
]


def run_checks(live=False):
    get_response = None
    reset_chat = None

    if live:
        from src.chatbot import get_chatbot_response, reset_chat
        get_response = get_chatbot_response

    passed = 0

    print("=" * 72)
    mode = "LIVE + RAG" if live else "OFFLINE RAG"
    print(f"CyberSafe Assistant — Automated Sample Check ({mode})")
    print("=" * 72)

    for label, question, keywords in SAMPLE_CHECKS:
        context = retrieve_context(question, top_k=3)
        ctx_lower = context.lower()

        rag_ok = any(keyword in ctx_lower for keyword in keywords)

        if live and get_response:
            reset_chat()
            answer = get_response(question)
            ans_ok = bool(answer and len(answer.strip()) > 20)

            ok = rag_ok and ans_ok
            detail = (
                f"RAG={'OK' if rag_ok else 'MISS'} "
                f"| Reply={len(answer)} chars"
            )
        else:
            ok = rag_ok
            detail = (
                f"Top-3 context retrieved "
                f"({context.count('Question:')} FAQs)"
            )

        status = "PASS" if ok else "FAIL"

        if ok:
            passed += 1

        print(f"[{status}] {label:<28} | {detail}")

    print("-" * 72)
    percentage = passed / len(SAMPLE_CHECKS) * 100

    print(
        f"Summary: {passed}/{len(SAMPLE_CHECKS)} checks passed "
        f"({percentage:.0f}%)"
    )

    return 0 if passed == len(SAMPLE_CHECKS) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--live",
        action="store_true",
        help="Also call Gemini API live"
    )

    args = parser.parse_args()
    sys.exit(run_checks(live=args.live))
