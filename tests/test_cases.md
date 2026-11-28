# Cybersecurity Chatbot Test Cases

**Project:** Cybersecurity Awareness Assistant\
**Role:** Domain Specialist -- Dayana\
**Purpose:** Check whether the chatbot gives accurate, relevant, clear
and practical cybersecurity guidance.

## Testing instructions

1.  Run each question against the working chatbot.
2.  Compare its response with the expected answer and pass criteria.
3.  Mark PASS only if the response meets the criteria. Otherwise mark
    FAIL.
4.  Record the actual response and any issue. Do not mark tests as
    passed before running them.

## Test cases

### TC01 -- Identifying phishing

-   **Category:** Phishing & Scams
-   **User question:** I received an email from my bank asking me to
    verify my account through a link. Is it safe?
-   **Expected answer:** Explain that this may be phishing. Advise not
    to click the link or provide credentials. Verify the request through
    the bank's official app, website typed directly into the browser, or
    verified contact details.
-   **Pass criteria:** Identifies the risk and recommends independent
    verification.

### TC02 -- Accidentally clicking a suspicious link

-   **Category:** Phishing & Scams
-   **User question:** I accidentally clicked a suspicious link in
    WhatsApp. What should I do now?
-   **Expected answer:** Close the page and do not enter information or
    download anything. If credentials were entered, change the affected
    password through the official service and enable MFA. If a file was
    downloaded, scan the device using trusted, updated security
    software. If financial details were provided, contact the bank
    through official channels.
-   **Pass criteria:** Gives practical steps and distinguishes clicking
    from entering credentials or downloading a file.

### TC03 -- Weak password

-   **Category:** Password & Account Security
-   **User question:** My password is 12345678. Is it strong enough?
-   **Expected answer:** Explain that it is common and easy to guess.
    Recommend a long, unique password or passphrase and a reputable
    password manager.
-   **Pass criteria:** Clearly identifies the password as weak and
    recommends a stronger unique password.

### TC04 -- Reusing passwords

-   **Category:** Password & Account Security
-   **User question:** Can I use the same password for my Instagram and
    Gmail accounts?
-   **Expected answer:** Recommend a different password for every
    account. If one service is compromised, attackers may try the same
    password on other accounts.
-   **Pass criteria:** Advises against password reuse and explains why.

### TC05 -- Understanding MFA

-   **Category:** Multi-Factor Authentication
-   **User question:** Why do I need an OTP when I already have my
    password?
-   **Expected answer:** Explain that multi-factor authentication adds
    another verification step, so a stolen password alone may not be
    enough. Remind the user never to share an OTP or approval code.
-   **Pass criteria:** Explains the additional protection and warns
    against sharing codes.

### TC06 -- Lost authenticator device

-   **Category:** Multi-Factor Authentication
-   **User question:** I lost my phone, and my accounts use an
    authenticator app. How can I log in?
-   **Expected answer:** Recommend backup codes or another registered
    method, followed by the service's official account-recovery process.
    After access is restored, remove the lost device from account
    security settings and register a replacement authenticator.
-   **Pass criteria:** Recommends official recovery methods and does not
    suggest bypassing MFA.

### TC07 -- Possible malware

-   **Category:** Malware & Viruses
-   **User question:** My laptop suddenly became very slow after I
    downloaded a free application. Could it be malware?
-   **Expected answer:** Explain that malware is possible but slowness
    can have other causes. Recommend removing suspicious software and
    running a scan with trusted, updated security software. If active
    compromise is suspected, disconnect from the network and seek
    trusted technical support.
-   **Pass criteria:** Does not claim malware is certain and gives
    sensible safety steps.

### TC08 -- Limits of antivirus

-   **Category:** Malware & Viruses
-   **User question:** If I install antivirus software, does that mean
    hackers cannot attack my computer?
-   **Expected answer:** Explain that antivirus can detect or block many
    threats but cannot guarantee complete protection. Recommend software
    updates, unique passwords, MFA, cautious browsing and backups as
    additional safeguards.
-   **Pass criteria:** Does not promise total protection and mentions
    other security practices.

### TC09 -- Fake technical support

-   **Category:** Social Engineering
-   **User question:** Someone called me claiming to be Microsoft
    support and asked me to install remote-access software. Should I
    follow their instructions?
-   **Expected answer:** Advise not to install the software or grant
    remote access in response to an unsolicited call. End the call and
    contact the company using details from its official website. If
    access was already granted, end the session, remove unauthorised
    software and seek trusted technical help.
-   **Pass criteria:** Identifies the social-engineering risk and
    recommends independent verification.

### TC10 -- Urgent payment request

-   **Category:** Social Engineering
-   **User question:** My manager suddenly WhatsApped me asking for an
    urgent money transfer. What should I do?
-   **Expected answer:** Do not transfer money based only on the
    message. Verify through a separate trusted channel, such as calling
    the manager using a known number, and follow the organisation's
    payment approval process.
-   **Pass criteria:** Recognises urgency as a possible manipulation
    tactic and recommends independent verification.

### TC11 -- Public Wi-Fi and banking

-   **Category:** Internet & Wi-Fi Safety
-   **User question:** I'm using free Wi-Fi at a shopping mall. Can I
    access my online banking?
-   **Expected answer:** Explain that public Wi-Fi may be untrusted.
    Recommend mobile data or a trusted network for sensitive banking
    activity, using the bank's official app or correctly typed website,
    and avoiding suspicious network names.
-   **Pass criteria:** Explains the risk without claiming every public
    Wi-Fi network is malicious.

### TC12 -- Website padlock

-   **Category:** Internet & Wi-Fi Safety
-   **User question:** A website has a padlock symbol. Does that mean it
    is completely safe?
-   **Expected answer:** Explain that HTTPS/padlock indicates an
    encrypted connection, not that the website itself is legitimate.
    Recommend checking the domain carefully and avoiding unexpected
    links.
-   **Pass criteria:** Distinguishes connection encryption from website
    legitimacy.

### TC13 -- Sharing identity information

-   **Category:** Privacy & Personal Data
-   **User question:** Someone online asked me to send a picture of my
    identity card. Should I send it?
-   **Expected answer:** Advise not to send it until the recipient,
    purpose and necessity have been independently verified. Explain that
    identity documents can be misused. If disclosure is genuinely
    required, use the organisation's official secure channel and follow
    its instructions for limiting unnecessary information.
-   **Pass criteria:** Warns about identity misuse and recommends
    verification before disclosure.

### TC14 -- Password disclosure

-   **Category:** Privacy & Personal Data
-   **User question:** I accidentally shared my password with someone
    through a chat. What should I do?
-   **Expected answer:** Change the password immediately through the
    official service, sign out of other sessions if possible, enable
    MFA, and change the same password on any other accounts where it was
    reused. Contact affected providers through official channels if
    sensitive accounts may be at risk.
-   **Pass criteria:** Gives immediate protection steps and addresses
    password reuse.

### TC15 -- Software updates

-   **Category:** Device & Software Security
-   **User question:** My phone keeps asking me to update its software.
    Can I ignore the updates?
-   **Expected answer:** Explain that updates often fix security
    weaknesses and bugs. Recommend installing updates through the
    device's official settings or software provider, and enabling
    automatic updates where appropriate.
-   **Pass criteria:** Explains the security value of updates and
    recommends official update channels.

## Results recording sheet

Complete this table only after testing the chatbot.

| Test ID | Result (PASS/FAIL) | Actual response / issue observed |
|---------|--------------------|----------------------------------|
| TC01 | PASS | It is not safe. This sounds like a phishing attempt. Banks typically do not ask you to verify your account by clicking a link in an email. Here is what you should do: -Do not click the link or download anything. -Do not enter any information or provide your password. -Check the sender through a separate trusted channel (like calling your bank using the official number on the back of your card. -Visit your bank's official website by typing the address yourself. -Report and delete the suspicious message. |
| TC02 | PASS | Here is what you do right now: 1.Close the page immediately and do not enter any information or download files. 2.If you enter a password, change it immediately from the official website and enable multi-factor authentication. 3.If you download a file, run a security scan and seek trusted technical help if needed. |
| TC03 | PASS | No, 12345678 is not strong enough. A strong password should be long, unique to one account, and difficult to guess. Instead of simple sequences, try using a long passphrase made from unrelated words, which can be easier to remember. You can also use a password manager to generate and store strong password securely. |
| TC04 | PASS | No, you should not use the same password for different accounts. Use a different password for every account. If one service is breached, attackers may try the exposed password on your other accounts, putting both your Instagram and Gmail at risk. |
| TC05 | PASS | An OTP is part of Multi-Factor Authentication (MFA), which is much better than using only a password. MFA provides an additional layer of protection, meaning a stolen password alone is not enough for an attacker to access your account. You should use MFA wherever it is available, especially for your email and financial accounts. |
| TC06 | PASS | Here is what you should do: -Use the account's official recovery process or a backup method you set up earlier, such as backup codes or another registered device. -Contact the service through its official support channel if needed. -Once you regain access, remove the lost device and register a replacement. |
| TC07 | PASS | Yes, it could be malware. Malware is software designed to harm a device, disrupt its operation, spy on users, or access information without permission, and it can arrive through unsafe downloads. Here are the practical staps you should take: -Stop using the device for sensitive activities and disconnect it from the network if you suspect an active infection. -Run a scan using trusted, updated security software and follow its removal guidance. -Change important passwords from a different, trusted device if they may have been exposed. -Seek professional help if the problem continues. |
| TC08 | PASS | No, antivirus software cannot guarantee complete protection from every cyberattack. While it can detect and block many known threats, you should also take these practical steps: -Keep your software updated. -Use strong, unique password and Multi-Factor Authentication (MFA). -Back up your important files regularly. -Always be careful with links, attachments, and downloads. |
| TC09 | PASS | No, you should not follow their instructions. This sounds like a fake technical support scam, where someone pretends to be a tech support worker and claims your device has a problem to pressure you into installing remote-access software, revealing passwords, or paying money. Here is what you should do: -End the contact immediately. -Do not install remote-access software or share any passwords. -Reach out to the company only using its official website or phone number if you believe there is a genuine issue. |
| TC10 | PASS | This sounds like a suspicious request. Please follow these practical steps: -Do not make any money transfer. -Check the sender through a separate, trusted channel (such as calling your manager directly on their phone number or talking to them in person) to verify if the request is real. -Report or delete the suspicious message. If you have already shared any sensitive financial information or transferred money, act quickly and contact your bank through its official channel immediately. |
| TC11 | PASS | No, you should avoid accessing highly sensitive accounts or making financial transactions on public Wi-Fi if you cannot verify the network;s security. Public Wi-Fi can be useful, but you should not assume every hotspot is trustworthy. It is much safer to use your mobile data for important transactions when possible. |
| TC12 | PASS | No, a padlock symbol does not mean the website is completely safe. A padlock symbol and HTTPS show that the connection is encrypted, but they do not prove that the website itself is honest. You should still check that the web address is correct and remain cautious of misspelled or unfamiliar domain names. |
| TC13 | PASS | No, you should not send a picture of your identity card. Personal information like your ID can be misused for identity theft, scams, account takeover, unwanted tracking, or impersonation. You should always share only what is necessary and check who is asking for it and why. |
| TC14 | PASS | Act quickly! Here are the practical steps you should take: 1.Change your password immediately: Go directly to the official website or app, change your password, and sign out of other sessions if the option is available.2.Enable multi-factor (MFA) to add an extra layer of security. 3.Check your accounts: Review your recovery details and recent account activity. 4.Update reused passwords: If you used that same password for any other accounts, change them immediately as well. |
| TC15 | PASS | No, you should not ignore the updates. Software updates often fix security weakness and vulnerabilities that attackers could exploit. Keeping your operating system, browser apps, and security software updated helps protect your device against know and newly discovered threats. Whenever practical, you should install updates from the device provider and enable automatic updates.|

## Notes and limitations

-   These are proposed test cases, not actual chatbot test results.
-   A test must not be marked PASS until it has been run against the
    working chatbot.
-   The chatbot should provide general cybersecurity awareness guidance,
    never request passwords or OTPs, and direct users to official
    service providers for account-specific action.
-   If a question is outside the chatbot's scope or available knowledge,
    it should say so rather than invent an answer.

## Automated RAG Check Results

**Test script:** `tests/check_sample_questions.py`  
**Test mode:** Offline RAG Check  
**Date:** 27 November 2026

| Sample Question | Result |
|---|---|
| Phishing (EN) | PASS |
| Weak Password (BM/Manglish) | PASS |
| MFA / OTP (EN) | PASS |
| Malware (BM) | PASS |
| Public Wi-Fi (EN) | PASS |
| Privacy / IC (EN) | PASS |
| Software Updates (EN) | PASS |
| Social Engineering (EN) | PASS |

**Overall Result:** 8/8 checks passed (100%).

**Observation:** All eight sample questions successfully retrieved the top three relevant FAQ results. At least one expected keyword was found in each retrieved context.

**Limitation:** This offline test checks FAQ retrieval only. It does not evaluate the accuracy or quality of Gemini-generated answers.

### Live RAG Check Results

**Test mode:** Live RAG Check (Gemini API)  
**Date:** 27 November 2026

| Sample Question | Result |
|---|---|
| Phishing (EN) | PASS |
| Weak Password (BM/Manglish) | PASS |
| MFA / OTP (EN) | PASS |
| Malware (BM) | PASS |
| Public Wi-Fi (EN) | PASS |
| Privacy / IC (EN) | PASS |
| Software Updates (EN) | PASS |
| Social Engineering (EN) | PASS |

**Overall Result:** 8/8 checks passed (100%).

**Observation:** All eight questions successfully retrieved FAQ context and received generated responses from Gemini. All responses contained more than 20 characters.

**Limitation:** This automated check validates retrieval and response generation, not the factual accuracy or completeness of each answer.
