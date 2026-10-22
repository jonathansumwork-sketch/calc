# Order portal backend/database/auth/file-storage options (state as of 22 Oct 2026)

FX used: 1 USD = 1.4217 AUD (2026-10-21) — [Frankfurter API](https://api.frankfurter.dev/v1/latest?from=USD&to=AUD). All AUD figures are USD x 1.4217, excl. GST. Pricing pages were fetched 22 Oct 2026 via a summarising fetch tool; items marked UNVERIFIED could not be confirmed on a primary page.

## 1. Free tier limits, cheapest paid plan, pausing, DB size, MAU, storage, egress

### Takeaway
Supabase Pro (US$25, ~A$36/mo) is the only option that bundles Postgres + auth + 100GB files + 250GB egress in a Sydney region with no pausing. Free tiers of Supabase (pauses after 1 week inactivity, no backups) and Appwrite (freezes at limit) are unsuitable for a live order portal. Neon is database-only (plus beta-ish managed auth); R2/B2 are the cheap file stores.

### Cited Findings
**Supabase**
- Free: US$0; 500MB DB, 1GB file storage, 5GB egress, 50,000 MAU; paused after 1 week inactivity; max 2 active projects; no backups — [Supabase pricing](https://supabase.com/pricing)
- Pro: from US$25/mo (~A$35.5); 8GB DB then $0.125/GB; 100GB files then $0.0213/GB; 250GB egress then $0.09/GB (cached egress $0.03/GB); 100,000 MAU then $0.00325/MAU; never paused; $10/mo compute credit covering one Micro instance; spend cap on by default (can be turned off) — [Supabase pricing](https://supabase.com/pricing)
- Team: from US$599/mo (~A$852); same base quotas, 14-day backups — [Supabase pricing](https://supabase.com/pricing)
- Extra compute beyond the credit starts at $10/mo (Micro) per project — [Supabase pricing](https://supabase.com/pricing)

**Firebase (Spark/Blaze)**
- Firestore Spark free: 1GiB stored, 10GiB/mo egress, 20K writes/day, 50K reads/day, 20K deletes/day; Blaze = same free amounts then Google Cloud rates — [Firebase pricing](https://firebase.google.com/pricing)
- Cloud Storage free quota (5GB stored, 100GB/mo download, 5K uploads, 50K downloads per month) applies ONLY to buckets in us-central1, us-west1, us-east1 — i.e. a Sydney bucket gets no free quota — [Firebase pricing](https://firebase.google.com/pricing)
- Auth: 50K MAU free then Google Cloud (Identity Platform) pricing; SAML/OIDC 50 free; phone auth billed per SMS — [Firebase pricing](https://firebase.google.com/pricing)
- Legacy appspot buckets listed at $0.026/GB stored, $0.12/GB downloaded — [Firebase pricing](https://firebase.google.com/pricing). A Dec 2022 archived GCS snapshot shows Sydney Standard at $0.023/GB-mo (old, verify) — [Wayback of GCS pricing](https://webcf.waybackmachine.org/web/20221229152713/https://cloud.google.com/storage/pricing)
- No fixed monthly fee; Blaze is pure pay-as-you-go (Spark is free but capped)

**Appwrite Cloud**
- Free org: "100% free"; at a resource limit the project freezes and Console goes read-only — [Appwrite pricing](https://appwrite.io/pricing)
- Pro: Sept 2025 changelog says price rose $15 -> $25/mo, bandwidth 300GB -> 2TB/project, per-project not per-seat; storage 150GB, 200K MAU; overage $15/100GB bandwidth, $2.8/100GB storage. Older pages still show $15/300GB (CONFLICT; treat $25 as current but re-verify) — [Appwrite changelog 2025-09-01 / search summary](https://appwrite.io/changelog/entry/2025-09-01.md), [announcing Pro](https://appwrite.io/blog/post/announcing-appwrite-pro)
- Databases: serverless with $10 compute credit; dedicated tiers $10/mo to $4,099/mo; PITR is +20% of base on dedicated — [Appwrite pricing](https://appwrite.io/pricing)
- Pro has budget cap; hitting cap denies API access — [Appwrite billing docs](https://appwrite.io/docs/advanced/billing/pro)

**PocketBase**
- Open source single-binary backend: embedded SQLite, REST/realtime, built-in dashboard, auth; files stored locally in pb_data; current v0.40.5; docs say pre-v1.0 with no backwards-compat guarantee and "NOT recommended for production critical applications yet"; manual migrations from time to time — [PocketBase docs](https://pocketbase.io/docs/)
- No licence fee; cost = your own VPS/hosting (not researched, see Gaps)

**Neon (Postgres)**
- Free: 100 CU-hours/project, 1GB/project (20GB account), 6-hour history, scale-to-zero after 5 min (cannot be disabled) — [Neon pricing](https://neon.com/pricing)
- Launch: pay-as-you-go $0.106/CU-hour; Scale $0.222/CU-hour; storage $0.35/GB-month; history up to 7 days (Launch) / 30 days (Scale); instant restore $0.20/GB-mo; Launch scale-to-zero can be disabled — [Neon pricing](https://neon.com/pricing)
- Neon Auth (Managed Better Auth): 60K MAU/project free, up to 1M on paid; no separate price listed — [Neon pricing](https://neon.com/pricing)
- Neon Object Storage listed at $0.023/GB-mo (5GB free) but NOT available in Sydney region — [Neon regions](https://neon.com/docs/introduction/regions)

**Cloudflare R2 / D1**
- R2: $0.015/GB-mo Standard, $0.01 IA ($0.01/GB retrieval); Class A $4.50/M, Class B $0.36/M; egress free; free tier 10GB, 1M A, 10M B — [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
- D1: Paid plan 25B rows read & 50M rows written/mo incl.; storage 5GB incl. then $0.75/GB-mo; Free plan 5GB total, 5M reads/100K writes per day — [D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/)

**Backblaze B2**
- $6.95/TB-mo; egress free up to 3x average monthly stored then $0.01/GB; free egress via partner CDNs (incl. Cloudflare); no minimum duration; first 10GB free; Class A/B/C calls free, Class D $0.004/10K — [Backblaze pricing](https://www.backblaze.com/cloud-storage/pricing)

**AWS Cognito**
- Lite 10,000 MAU free (50K for pools created before 22 Nov 2024) then $0.0055/MAU; Essentials 10K free then $0.015; Plus $0.020 — [Cognito pricing](https://aws.amazon.com/cognito/pricing/)
- S3: first 100GB/mo internet egress free; N. Virginia egress $0.09/GB; reads $0.0004/1K, writes $0.005/1K — [AWS S3 pricing](https://aws.amazon.com/s3/pricing/), [Upstash 2026 S3 guide](https://upstash.com/blog/aws-s3-pricing-explained-2026). Sydney-specific storage/egress figure NOT confirmed on primary page (one third-party table: Sydney ~$0.025/GB-mo, old — [Enterprise Storage Forum](https://www.enterprisestorageforum.com/cloud/aws-s3-pricing/))

**Clerk (auth only)**
- Hobby: 50,000 MRU free; Pro $25/mo ($20 annual); $0.02/MRU for 50-100K; Organizations add-on $100/mo ($85 annual) w/ 100 retained orgs free — [Clerk pricing](https://clerk.com/pricing). Billed on "monthly retained users", not MAU.

### Inferences
- For 50-500 clients, every auth option is effectively free (all under the 10K-50K free MAU thresholds). Auth is not a cost driver; choose on features.
- Supabase Free is a prototype tier only (pausing + no backups); a production portal needs Pro.
- Firebase's free Storage quota is irrelevant for an Australian deployment because it's US-bucket-only.

### Gaps
- Appwrite's current exact Free-plan numbers and Pro compute/DB overage rates (compare-plans table not retrievable).
- Auth0 pricing not researched.
- Supabase compute tier prices above Micro (Small etc.) not retrieved.

## 2. Cost to store and serve 50GB / 200GB / 500GB of artwork (monthly, USD; storage + egress)

### Takeaway
Cloudflare R2 (~US$0.60 / $2.85 / $7.35) and Backblaze B2 (~$0.28 / $1.39 / $3.48) are an order of magnitude cheaper than Firebase/S3 once egress is included, and have free/cheap egress. Supabase Storage is cheap too (included 100GB, $0.0213/GB) but egress beyond 250GB/mo is $0.09/GB.

### Cited Findings (calculations from the cited list prices; egress scenario = downloads equal to 1x stored per month, plus ops ignored as negligible)
| Option | 50GB | 200GB | 500GB | Basis |
|---|---|---|---|---|
| R2 Standard | $0.60 | $2.85 | $7.35 | (GB-10 free) x $0.015; egress $0 — [R2](https://developers.cloudflare.com/r2/pricing/) |
| B2 | ~$0.28 | ~$1.39 | ~$3.48 | (GB-10 free) x $6.95/1000 or full GB; egress free up to 3x — [B2](https://www.backblaze.com/cloud-storage/pricing) |
| Supabase Storage (on Pro) | $0 extra | $2.13 | $8.52 | 100GB incl., $0.0213/GB over; egress 1x: $0 / $0 / $7.50 cached or $22.50 uncached (250GB incl., $0.03 cached/$0.09 uncached) — [Supabase](https://supabase.com/pricing) |
| Firebase Storage | $1.30 + $6 egress = $7.30 | $5.20 + $24 = $29.20 | $13 + $60 = $73 | $0.026 stored, $0.12 egress (legacy-bucket list prices; Sydney bucket rate UNVERIFIED, may differ) — [Firebase](https://firebase.google.com/pricing) |
| Appwrite Pro | $0 extra | $1.40 | $9.80 | 150GB incl., $2.8/100GB; 2TB bandwidth incl. — [changelog](https://appwrite.io/changelog/entry/2025-09-01.md) |
| S3 Sydney | ~$1.25 | ~$5 | ~$12.50 | assumes $0.025/GB-mo (UNVERIFIED); egress ~$0.09-0.114/GB after 100GB free (Sydney rate UNVERIFIED) -> roughly $0 / $9-11 / $36-46 at 1x |

AUD multiply by 1.4217 (e.g. R2 500GB ≈ A$10.45; B2 500GB ≈ A$4.95; Firebase 500GB w/1x egress ≈ A$104).

### Inferences
- Even at 5x egress, R2 stays storage-only cost; B2 costs only $0.01/GB beyond 3x. Egress is the swing factor for S3/Firebase/Supabase.
- R2 and B2 have no Sydney region selection in the sources I retrieved (R2 offers location hints/jurisdictions; not verified here) — latency to AU users is via Cloudflare's edge; see Section 3.

### Gaps
- Current Sydney S3 and GCS price tables did not render; those rows are estimates.
- R2/B2 regional placement (APAC) not verified. B2 regions (US/EU, possibly others) not confirmed.

## 3. Australian (Sydney) region availability

### Takeaway
Sydney is available for Supabase (ap-southeast-2), Neon Postgres + Auth, Firestore (Sydney and Melbourne), AWS, and GCS. Appwrite Cloud, R2 and B2 region availability for Sydney was not confirmed.

### Cited Findings
- Supabase: "Oceania (Sydney) ap-southeast-2" listed under specific regions — [Supabase regions](https://supabase.com/docs/guides/platform/regions)
- Neon: AWS Sydney (aws-ap-southeast-2) available for Postgres and Managed Better Auth; Object Storage, Functions, AI Gateway, Realtime NOT yet there — [Neon regions](https://neon.com/docs/introduction/regions)
- Firestore: australia-southeast1 (Sydney) and australia-southeast2 (Melbourne) — [Firestore locations](https://firebase.google.com/docs/firestore/locations)
- Firebase Storage free quota excludes non-US buckets — [Firebase pricing](https://firebase.google.com/pricing)
- GCS Sydney (australia-southeast1) exists as region/dual-region — [search summary of GCS pricing](https://cloud.google.com/storage/pricing)
- Appwrite: regions page did not list regions in retrievable text — [Appwrite docs](https://appwrite.io/docs/advanced/platform/regions)

### Inferences
- A Supabase (Sydney DB+auth) + R2 (files) hybrid is plausible, but Supabase Storage in Sydney keeps everything in one region.
- AWS Sydney has data-residency options for Cognito/S3/RDS (AWS regional availability not fetched; general knowledge).

### Gaps
- Appwrite Cloud Sydney; R2/B2 AU data location; D1 location control.

## 4. Row-level security, per-customer isolation, price lists, CSV import/export

### Takeaway
Supabase and Neon (plain Postgres) support native Postgres RLS, which maps cleanly to per-customer data and per-customer price tables. Firebase uses Security Rules; PocketBase uses per-collection API rules; D1 (SQLite) has no RLS. I did not retrieve primary documentation on these features this session.

### Cited Findings
- PocketBase has a dashboard, REST API, auth management and SQLite — [PocketBase docs](https://pocketbase.io/docs/) (RLS/CSV specifics not in retrieved text)
- Supabase and Neon are Postgres-based, per pricing pages — [Supabase](https://supabase.com/pricing), [Neon](https://neon.com/pricing)

### Inferences (uncited general knowledge, verify before relying)
- Postgres RLS policies (customer_id = auth.uid()) plus a customer_prices(customer_id, sku, price) table gives customer-specific price lists; Supabase dashboard supports CSV import/export per table and standard pg_dump/COPY gives full export. Firestore has no native CSV tooling or SQL joins (price-list/stock reporting harder; needs custom scripts). PocketBase supports collection rules and CSV needs scripting/extension.

### Gaps
- No primary-source verification of RLS, CSV import/export tooling per platform.

## 5. Backups / point-in-time recovery

### Takeaway
Supabase: no backups on Free, daily 7 days on Pro, PITR is a paid add-on (~$100/mo per 7 days) needing at least Small compute. Neon gives PITR-style history on all plans (6h Free; 7d Launch; 30d Scale). PocketBase backups are DIY.

### Cited Findings
- Supabase Pro 7 days daily backups, Team 14, Enterprise up to 30; Free no automatic backups; PITR add-on for Pro+, requires >= Small compute, ~$100/mo (7d), $200 (14d), $400 (28d), RPO ~2 min; storage objects not included in backups (metadata only); project inaccessible during restore — [Supabase backups docs](https://supabase.com/docs/guides/platform/backups)
- Neon history window 6h / up to 7d / up to 30d; instant restore $0.20/GB-mo — [Neon pricing](https://neon.com/pricing)
- Appwrite dedicated DB PITR +20% of base — [Appwrite pricing](https://appwrite.io/pricing)

### Inferences
- Supabase backups do not cover artwork files; a bucket-to-R2/B2 copy job or using R2/B2 as primary store (with versioning) covers this.
- Budget realistic Supabase cost with PITR: $25 + $100 + Small compute upgrade, i.e. >US$130 (A$185+); Pro daily backups (included) probably enough for a small order portal.

### Gaps
- Firebase Firestore backup/PITR pricing not retrieved. Cloudflare D1 Time Travel pricing not retrieved. Small compute price not retrieved.

## 6. Operational burden, dashboard quality, lock-in, exit

### Takeaway
Supabase/Appwrite/Firebase are managed with dashboards; PocketBase is self-run (server, updates, backups, pre-1.0 caveat) and the heaviest burden for a non-developer team. Postgres-based options have the easiest exit (standard dumps).

### Cited Findings
- PocketBase: pre-v1.0, manual migrations, not recommended for production-critical apps — [PocketBase docs](https://pocketbase.io/docs/)
- Appwrite is self-hostable alternative (Cloud is managed) — [Appwrite docs](https://appwrite.io/docs/advanced/platform/regions)
- Clerk bills per retained user and is auth-only; separate DB needed — [Clerk](https://clerk.com/pricing)

### Inferences (uncited judgment)
- Lowest lock-in: Supabase/Neon (standard Postgres; Supabase auth/storage APIs have some coupling). Highest: Firebase (Firestore NoSQL, Security Rules), D1/Workers (Cloudflare-specific). A non-developer team will need a developer/agency for any option; no option removes that.

### Gaps
- No independent dashboard-quality comparisons retrieved.

## 7. Realistic monthly cost scenarios (50-500 clients, 200-2000 orders/mo, 50-500GB)

### Takeaway
Order volume (≤2000 orders/mo) is trivial for every DB; cost is dominated by plan base fee and artwork egress. Supabase Pro is about US$25-35 (A$36-50), hybrid with R2 about US$25 + $0.6-7.35, Firebase can balloon with egress.

### Cited Findings / calculations (USD, ex-GST; derived from lists above)
- Supabase Pro all-in-one: $25 base (includes Micro compute credit, 8GB DB, 100GB files, 250GB egress). 50GB: ~$25 (A$36); 200GB: ~$27 (A$38); 500GB: ~$33.5-50 (A$48-71) depending on egress 1x with cached/uncached — [Supabase](https://supabase.com/pricing)
- Supabase Pro + R2 for files: $25 + $0.60 / $2.85 / $7.35 = $25.6 / $27.9 / $32.4 (A$36 / A$40 / A$46) — [Supabase](https://supabase.com/pricing), [R2](https://developers.cloudflare.com/r2/pricing/)
- Neon Launch (DB) + R2 + Clerk/Neon Auth: DB compute at $0.106/CU-hr (~$77/mo if 1 CU always on, 730h; ~less if scale-to-zero) + $0.35/GB DB storage; + R2 — [Neon](https://neon.com/pricing). Cost ~ $5-80 + files; (DB size small).
- Appwrite Pro: $25 + overage (A$36-50 for 500GB at $9.80 storage) — [changelog](https://appwrite.io/changelog/entry/2025-09-01.md)
- Firebase Blaze: Firestore reads/writes at 2000 orders/mo negligible (free quota covers); main cost Storage $7-73/mo at 50-500GB with 1x egress — [Firebase](https://firebase.google.com/pricing)
- Cognito: 10K free MAU covers 500 clients ($0) — [Cognito](https://aws.amazon.com/cognito/pricing/)
- PocketBase: software free; VPS cost not researched.

### Inferences
- At this scale, a US$25/mo (~A$36) Supabase Pro with R2/B2 for artwork is the most cost-effective managed stack; total ~A$36-50/mo. Free tiers are not viable for production.
- Supabase Pro spend cap on by default: could block uploads if exceeded; consider turning off cap for production or monitoring.

### Gaps
- Real egress volume unknown (assumed 1x stored per month); GST and card FX fees not included; AWS RDS pricing not researched; VPS costs for PocketBase not researched; Auth0 not researched; independent 2026 comparisons not retrieved.
