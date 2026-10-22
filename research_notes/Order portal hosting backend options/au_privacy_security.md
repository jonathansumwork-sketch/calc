# Australian data residency, privacy and security requirements for a small business customer order portal

(Research notes, as of 22 Oct 2026. Not legal advice. Search-tool summaries were used for several items; items not confirmed on a primary page are flagged in Gaps.)

## 1. Does the Privacy Act / APPs (APP 8, APP 11) apply to a small business; exemption rules; reforms; NDB scheme

### Takeaway
A business with annual turnover of $3M or less is generally outside the Privacy Act (and so outside the APPs and the NDB scheme), but there are important exceptions and a voluntary opt-in, and the blanket exemption has NOT been repealed as far as found (tranche 2 pending). If the business is over $3M, or falls in an exception, APP 8 (cross-border) and APP 11 (security) apply.

### Cited Findings
- Small business = annual turnover $3M or less (all income, excluding assets/capital gains). Most small businesses are not covered by the Privacy Act. — [OAIC small business guidance](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business)
- Covered regardless of turnover: health service providers; businesses trading in personal information; Commonwealth contracted service providers; related bodies corporate of covered businesses; residential tenancy database operators, credit reporting bodies, AML/CTF reporting entities, Consumer Data Right accredited entities; businesses prescribed by regulation. — [OAIC](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business)
- A small business can voluntarily opt in to the Privacy Act; OAIC recommends this as it can build customer trust. — [OAIC](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business)
- The Notifiable Data Breaches scheme applies to "any organisation or agency the Privacy Act 1988 covers"; a notifiable breach is unauthorised access/disclosure/loss likely to result in serious harm (examples: hacked database, lost device, info sent to wrong person). So it follows Privacy Act coverage. — [OAIC NDB scheme](https://www.oaic.gov.au/privacy/notifiable-data-breaches/about-the-notifiable-data-breaches-scheme)
- Contracted service provider exception matters for this business: if it supplies services to Commonwealth agencies under a contract, it is covered regardless of turnover. — [OAIC](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business)
- APP 8.1: before disclosing personal information to an overseas recipient, take reasonable steps to ensure the recipient does not breach the APPs (other than APP 1); s 16C makes the Australian entity accountable for the overseas recipient's acts; exceptions exist. OAIC Chapter 8 guidelines v1.3 dated October 2025. — [OAIC APP Guidelines Ch 8 (Oct 2025 v1.3)](https://www.oaic.gov.au/__data/assets/pdf_file/0036/256959/APP-Guidelines-Chapter-8-Cross-border-disclosure-of-personal-information-October-2025-v1.3.PDF)
- OAIC position: where a third party exploits the entity's security to gain access, the entity is not treated as having "disclosed", but may breach APP 11 if it did not take reasonable steps to protect the information. — via search summary of [OAIC Ch 8](https://www.oaic.gov.au/privacy/australian-privacy-principles-guidelines/chapter-8-app-8-cross-border-disclosure-of-personal-information/)
- Privacy and Other Legislation Amendment Act 2024: Royal Assent 10 Dec 2024; most provisions effective Dec 2024; statutory tort for serious invasions of privacy commenced 10 June 2025. — [Coleman Greig](https://colemangreig.com.au/insights/blogs/concerns-for-business-under-the-privacy-and-other-legislation-amendment-act-2024), [Warlows Legal](https://warlowslegal.com.au/?p=17357)
- Tranche 1 did not remove the small business exemption (s 6D); the Parliamentary Library Bills Digest notes removal was not implemented in the Bill. — [APO Bills Digest](https://apo.org.au/sites/default/files/resource-files/2024-09/apo-nid328549.pdf)
- Tranche 2 status (secondary sources only): removal of the blanket $3M exemption listed as proposed, not law; government agreed in principle subject to consultation. — [Scalesuite](https://www.scalesuite.com.au/resources/privacy-act-changes-for-smes), [CGW](https://cgw.com.au/?p=35768)
- What did change on 1 July 2026 (AML/CTF tranche 2): small businesses providing newly regulated designated services (e.g. real estate, lawyers, accountants, dealers in precious metals/stones) lose the exemption for AML/CTF-related personal information. Not relevant to a signage company. — [HWL Ebsworth](https://hwlebsworth.com.au/small-businesses-big-change-privacy-obligations-under-tranche-2-of-the-aml-ctf-reforms/), [QLS guide](https://www.qls.com.au/getmedia/58d2d0fb-424a-442d-8f0b-9672b8b0e84f/AML-CTF_Starter-Guide.pdf?ext=.pdf)
- Conflicting: one vendor site (Cybercraft) claims full removal from 1 July 2026; this contradicts the sources above and is likely inaccurate — [Cybercraft](https://www.cybercraft.net/privacy-act-compliance) vs [Scalesuite](https://www.scalesuite.com.au/resources/privacy-act-changes-for-smes)
- Automated decision-making transparency obligations start 10 Dec 2026 (only relevant if portal uses automated decisions about individuals; applies to covered entities) — [EPIC IT](https://www.epicit.com.au/?p=15345)

### Inferences
- A small signage firm with turnover under $3M that is not a health provider, doesn't trade in personal data, and has no Commonwealth contracts is probably not legally bound by the APPs/NDB, but customers (councils, healthcare) often contractually flow them down, and opting in is cheap insurance. Council contracts could be state/local (not "Commonwealth contracted service provider"), so state privacy laws flowing via contract are a separate matter.
- The data held (business contact names, emails, order details, artwork) is mostly low-sensitivity personal information; artwork files may contain third-party personal data or sensitive content (e.g. healthcare signage), which is worth checking.
- Seek legal advice on: turnover threshold (including related bodies corporate), whether opt-in is advisable, and contractual flow-down clauses.

### Gaps
- Did not confirm via a primary source (Attorney-General's Department / Parliament) the exact tranche 2 status as at Oct 2026; secondary sources only.
- Did not confirm whether the statutory tort applies to small businesses (not found).
- OAIC APP 11 guideline text and exact NDB 30-day assessment timeframe not retrieved (the NDB page fetched did not state it; commonly understood as 30 days to assess, but unverified here).
- State-level privacy laws (e.g. NSW PPIP Act, Vic) affecting council customers not researched.

## 2. Is Australian data residency legally required, or best practice? What do large AU customers expect?

### Takeaway
For a private small business, the Privacy Act does not mandate onshore storage; it permits overseas disclosure subject to APP 8 accountability. Residency is mainly a customer/contract/procurement expectation (especially government-related), not a statutory rule for this business.

### Cited Findings
- APP 8 regulates, rather than prohibits, cross-border disclosure; entity remains accountable (s 16C) — [OAIC Ch 8](https://www.oaic.gov.au/__data/assets/pdf_file/0036/256959/APP-Guidelines-Chapter-8-Cross-border-disclosure-of-personal-information-October-2025-v1.3.PDF)
- AWS Melbourne region is in IRAP PROTECTED scope (Dec 2022 assessment), 139 services assessed at PROTECTED overall; illustrates the government-grade onshore benchmark customers may reference — [AWS Security Blog](https://aws.amazon.com/blogs/security/2022-h2-irap-report-is-now-available-on-aws-artifact-for-australian-customers)

### Inferences
- Large public-sector and health customers commonly ask in security questionnaires where data is hosted and whether it leaves Australia; some require onshore hosting by policy or contract (not verified with sources here). Sydney/Melbourne hosting is the low-friction answer, and "data stored in Sydney, but some processors/support access offshore" must be disclosed accurately.
- Be careful: even if the DB is in Sydney, email providers, error monitoring, analytics, CDN logs, and platform support may process data offshore.

### Gaps
- No primary source found on specific council, healthcare, transport or utility procurement residency requirements (e.g. state government ICT policies, health records laws such as My Health Records Act offshore prohibition, which applies to health records not signage orders). Recommend asking target customers for their vendor questionnaire.

## 3. Platform region comparison (Australia)

### Takeaway
Supabase (Sydney), Firebase/GCP (Sydney and Melbourne), AWS (Sydney and Melbourne) and Vercel (syd1 compute) and Fly.io (Sydney) and Netlify (Sydney functions) can place compute/data in Australia; Render has no Australian region; Cloudflare is global edge and can't guarantee Australian-only R2 storage (location hint only). Supabase and Vercel are different layers (DB vs front-end), so residency needs to be checked per component.

### Cited Findings
- Supabase: specific region "Oceania (Sydney)" ap-southeast-2 (AWS); no Melbourne; general regions (Americas, Europe, APAC=Singapore) exist, so choose the specific Sydney region for residency; general regions don't support read replicas. No plan restriction mentioned on the regions page. — [Supabase regions](https://supabase.com/docs/guides/platform/regions)
- Firebase/Firestore: regional locations include australia-southeast1 (Sydney) and australia-southeast2 (Melbourne); default resource location setting is immutable once chosen. — [Firestore locations](https://firebase.google.com/docs/firestore/locations)
- AWS: Sydney (ap-southeast-2, since 2012) and Melbourne (ap-southeast-4, 3 AZs); Melbourne in IRAP PROTECTED scope. — [AWS Security Blog](https://aws.amazon.com/blogs/security/2022-h2-irap-report-is-now-available-on-aws-artifact-for-australian-customers), [Petri](https://petri.com/aws-launches-cloud-region-melbourne/)
- Vercel: compute region syd1 (ap-southeast-2) among 19 compute regions; Functions DEFAULT to iad1 (Washington DC) unless changed; CDN has 126 PoPs globally, so cached content is served from global edges; failover for non-Enterprise may route traffic to other regions in listed priority (for default iad1 chain). Docs updated 2026-08-11. — [Vercel regions](https://vercel.com/docs/regions)
- Vercel multi-region functions need Pro/Enterprise (secondary, older source) — [Temperstack](https://www.temperstack.com/learn/vercel/configure-multi-region-functions/)
- Render: five regions: Oregon, Ohio, Virginia, Frankfurt, Singapore; none in Australia. — [Render regions](https://render.com/docs/regions)
- Fly.io: Sydney (syd) listed, with Managed Postgres support; no Melbourne. — [Fly.io regions](https://docs.fly.io/reference/regions)
- Netlify: Functions region can be set to Sydney (ap-southeast-2) in site settings (applies to all functions, requires redeploy) or per function in code; older forum posts say Pro plan was needed (may be outdated). Static assets are served via global CDN. — [Netlify functions config](https://docs.netlify.com/build/functions/configuration/), [Netlify forum](https://answers.netlify.com/t/changing-deployment-region/25265)
- Cloudflare: Data Localization Suite (Regional Services incl. Australia since Sept 2022, Geo Key Manager, Customer Metadata Boundary) — [Cloudflare DLS](https://www.cloudflare.com/en-au/data-localization/), [IT Brief](https://itbrief.com.au/story/cloudflare-launches-data-localisation-suite). R2: location hints include `oc` (Oceania) and `apac` but hints are "best effort and not a guarantee"; jurisdictions available only eu, fedramp (Enterprise), us; Australia is NOT a jurisdiction. — [Cloudflare R2 data location](https://developers.cloudflare.com/r2/reference/data-location/)

### Inferences
- A defensible "Australian-resident" stack: Supabase Sydney (DB, Auth, Storage) + Vercel/Netlify functions pinned to Sydney, or Firebase australia-southeast1/2, or AWS Sydney/Melbourne. Cloudflare R2 shouldn't be described as guaranteed Australian-only storage; Cloudflare Workers/CDN will cache and process at global edge by default unless Regional Services (likely paid/Enterprise; unverified) is used. Render is out for residency.
- Front-end CDNs on Vercel/Netlify/Cloudflare cache public assets globally; fine if no personal data/artwork is cached publicly, but authenticated responses should be non-cacheable.

### Gaps
- Supabase paid-plan restrictions for Sydney: regions page shows none, but not verified against pricing (note Supabase free tier projects get paused; paid plan advisable for production). Supabase Storage/Edge Functions region behaviour not checked.
- Netlify current plan restrictions for region selection not confirmed on a current primary page.
- Cloudflare Regional Services plan requirements and Workers/D1 Australian placement not confirmed. Firebase Auth/Hosting/Cloud Functions regional detail not checked (Firebase Auth is global; unverified).
- Fly.io Melbourne absent; Fly Managed Postgres pricing not checked.

## 4. Compliance certifications and security-questionnaire expectations

### Takeaway
Supabase, Render and Vercel confirm SOC 2 Type 2; Supabase and Render confirm ISO 27001. Reports are often gated behind paid tiers/NDA. Netlify, Fly.io, Cloudflare, Google, AWS certifications were not confirmed in this research session (widely known to hold SOC 2/ISO 27001 but unverified here).

### Cited Findings
- Supabase: SOC 2 Type 2, ISO 27001, HIPAA (with BAA); report/certificate/BAA available to Team and Enterprise plan customers via dashboard; DPA available; regular penetration testing. — [Supabase security](https://supabase.com/security)
- Render: SOC 2 Type 2 and ISO/IEC 27001:2022 (Nov 2024); reports under NDA for Pro workspaces and higher (older docs said Organization/Enterprise). — [Render compliance](https://render.com/docs/certifications-compliance)
- Vercel: SOC 2 Type 2 (Security, Confidentiality, Availability); ISO 27001 not found in results. — [Vercel KB](https://vercel.com/kb/guide/is-vercel-soc-2-compliant)
- AWS provides IRAP assessment reports via AWS Artifact to Australian customers. — [AWS Security Blog](https://aws.amazon.com/blogs/security/2022-h2-irap-report-is-now-available-on-aws-artifact-for-australian-customers)

### Inferences
- Typical questionnaire asks (from general knowledge, unsourced): data location and sub-processors; encryption in transit/at rest; MFA/SSO; access control/least privilege; backup and restore/RTO-RPO; incident response and breach notification timelines; pen-test evidence; vulnerability patching; staff access/background checks; data retention/deletion on exit; insurance (cyber). Inheriting the platform's SOC 2/ISO 27001 is accepted as supporting evidence but does not certify the small business itself; Essential Eight alignment is a commonly-cited Australian framework.

### Gaps
- Netlify, Fly.io, Cloudflare, Google Cloud/Firebase certification pages not fetched; AWS/GCP general certs unverified here.
- No sourced list of what AU council/health questionnaires ask.

## 5. Basic security for customer logins and file uploads (MFA, verification, file limits, malware scanning) and cost

### Takeaway
Use managed auth with email verification and optional TOTP MFA, restrict file types/sizes server-side, store uploads in private buckets with signed URLs, and add malware scanning (ClamAV or WAF content scanning). Cost for the basics is mostly near-zero to low; managed scanning adds cost/ops effort. Specific dollar figures were not verified.

### Cited Findings
- Supabase Auth supports MFA via authenticator app (TOTP) and phone code; plan/pricing for MFA not stated on the page (phone SMS would incur provider costs; unverified). — [Supabase MFA docs](https://supabase.com/docs/guides/auth/auth-mfa)
- Cloudflare WAF "malicious uploads" detection scans uploaded content with an AV engine for requests through Cloudflare-proxied routes; availability by plan not confirmed; unclear for direct-to-storage uploads. — [Cloudflare malicious uploads](https://developers.cloudflare.com/waf/detections/malicious-uploads)
- Google's reference architecture: upload to an unscanned bucket, event-triggered ClamAV scanner service, clean files moved to a separate bucket. — [Google Cloud architecture](https://docs.cloud.google.com/architecture/automate-malware-scanning-for-documents-uploaded-to-cloud-storage)

### Inferences
- Practical baseline (unsourced best practice): email verification; TOTP MFA optional for customers and mandatory for staff/admin; rate limiting/CAPTCHA on login; row-level security so customers see only their own orders; allowlist file types for artwork (PDF, AI, EPS, SVG, PNG, JPG, TIFF; consider that SVG/PDF can carry active content), size cap, rename files, private bucket + short-lived signed URLs; quarantine-then-scan pattern. Malware scanning via self-hosted ClamAV costs a small always-on container (approx. low tens of dollars per month; estimate, unverified) vs. commercial scanning APIs priced per scan.

### Gaps
- No verified pricing for Supabase MFA/SMS, malware scanning services, or WAF tiers; ACSC Essential Eight / small business guidance not retrieved.
