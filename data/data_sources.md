# Cybersecurity Awareness Assistant — Dataset Sources

## Dataset overview

This dataset contains 40 original question-and-answer pairs across eight basic cybersecurity awareness categories: Phishing & Scams; Password & Account Security; Multi-Factor Authentication; Malware & Viruses; Social Engineering; Internet & Wi-Fi Safety; Privacy & Personal Data; and Device & Software Security. The answers are written in simple language for general users. They summarise public cybersecurity guidance rather than reproducing long passages.

## Sources consulted

1. **Cybersecurity and Infrastructure Security Agency (CISA).** *Secure Our World: 4 Easy Ways to Stay Safe Online* (tip sheet). Covers recognising and reporting phishing, strong passwords, password managers, MFA, and software updates.
   - https://www.cisa.gov/sites/default/files/2024-09/Secure-Our-World-4-Easy-Ways-Stay-Safe-Online-Tip-Sheet.pdf

2. **National Institute of Standards and Technology (NIST).** *How Do I Create a Good Password?* Updated 20 August 2025. Covers long passwords/passphrases, password managers, MFA, passkeys, and the relative security of authentication methods.
   - https://www.nist.gov/cybersecurity-and-privacy/how-do-i-create-good-password

3. **NIST.** *Multi-Factor Authentication.* Explains authentication factors, why MFA adds protection, and phishing-resistant authentication options.
   - https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/multi-factor-authentication

4. **Federal Trade Commission (FTC), Consumer Advice.** *Protect yourself from phishing scams* (April 2025). Covers common phishing approaches, avoiding suspicious links and attachments, independently verifying messages, and reporting phishing.
   - https://consumer.ftc.gov/consumer-alerts/2025/04/protect-yourself-phishing-scams

5. **FTC, Consumer Advice.** *How To Recognize and Avoid Phishing Scams.* Covers phishing signs, safe verification, and steps to take after responding to a phishing message.
   - https://consumer.ftc.gov/articles/how-recognize-avoid-phishing-scams

6. **FTC, Consumer Advice.** *Five ways to keep scammers and hackers away.* Covers account security, software updates, Wi-Fi/router security, device locks, and backups.
   - https://consumer.ftc.gov/consumer-alerts/2024/08/five-ways-keep-scammers-hackers-away

## How the sources were used

The sources above informed the general safety recommendations in the answers. The wording of each answer was written specifically for this dataset. Some entries combine basic cybersecurity concepts across the sources to provide a short, practical response. The dataset is educational and does not replace professional technical support or advice from a bank, service provider, or cybersecurity specialist.

## Dataset file

`cybersecurity_faq.csv` contains three columns: `Category`, `Question`, and `Answer`. There are 40 entries, with five question-answer pairs in each category.
