# Hosting platforms for a small-business customer order portal (Australia): Netlify, Vercel, Cloudflare, Firebase, AWS Amplify, Render, Railway, Fly.io

Research date: 2026-10-22. AUD figures are my own conversion at an ASSUMED rate of about 1 USD = 1.50 AUD (AUD/USD about 0.67). I did not verify the current exchange rate, so treat AUD as approximate. All prices are USD and exclude GST unless stated.

## 1. Pricing: free tier, cheapest paid plan, seats, limits, overages

### Takeaway
Pricing is mostly flat-fee plus metered usage. Vercel is the only one that charges per seat ($20 per developer). Netlify, Render and Railway Pro are flat per workspace with unlimited members. Cloudflare is the cheapest at $5 per month with no egress fees. Fly.io has no free tier and no dashboard-first model. I could not verify Render's per-instance prices or included bandwidth, or the Cloudflare/Netlify/Firebase free-tier commercial-use terms.

### Cited Findings

**Netlify**
- Credit-based plans: Free $0 (300 credits), Personal $9 (1,000 credits), Pro $20 (3,000 credits, "unlimited members"), Enterprise custom. Pro is a flat $20 with no per-seat charge listed. About A$30/month for Pro. — [Netlify pricing](https://www.netlify.com/pricing/)
- Credit costs: production deploy 15 credits; compute 10 credits/GB-hour; web requests 2 credits per 10,000; bandwidth 20 credits/GB; preview/branch/failed deploys and form submissions not metered. — [Netlify credit docs](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)
- Free plan has a "credit hard limit" with no auto-recharge. Pro has auto-recharge. Higher Pro tiers: 5,000 credits for $33, 10,000 for $63, 15,000 for $95, 20,000 for $126. Pro credit packs: 1,500 for $10. — [Netlify credit docs](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)
- Pro add-ons: extra concurrent builds $40/month each beyond those included. — [Netlify credit docs](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)
- Derived at the Pro pack rate (about $0.0067/credit): bandwidth about $0.13/GB, compute about $0.07/GB-hour, requests about $0.01 per 10,000, deploy about $0.10. — [Netlify pricing](https://www.netlify.com/pricing/)
- Function limits: sync 60 s, scheduled 30 s, background 15 min; payload 6 MB buffered. — [Netlify functions docs](https://docs.netlify.com/build/functions/optional-configuration/)

**Vercel**
- Hobby $0 (1 developer seat). Pro $20/month with $20 included usage credit, developer seats $20 each per month, unlimited free viewer seats, one billing seat. About A$30 base. — [Vercel pricing](https://vercel.com/pricing); [Hobby docs](https://vercel.com/docs/plans/hobby)
- Hobby included: 100 GB Fast Data Transfer, 1M CDN requests, 1M function invocations, 4 CPU-hrs, 360 GB-hrs memory; function max duration 300 s. Exceeding Hobby limits means waiting about 30 days; no purchase of extra usage. — [Vercel Hobby docs](https://vercel.com/docs/plans/hobby)
- Pro included 1 TB bandwidth and 10M CDN requests; overage from $0.15/GB, $2 per 1M requests, $0.60 per 1M invocations, $0.128/CPU-hour, $0.0106/GB-hr memory; uncapped pay-as-you-go (spend management configurable). — [Vercel pricing](https://vercel.com/pricing); [Hobby docs](https://vercel.com/docs/plans/hobby)
- Pro: 6,000 deployments/day; 1 day of runtime logs; email support. Hobby: 100 deployments/day, 1 hour logs, no email support. — [Vercel Hobby docs](https://vercel.com/docs/plans/hobby)
- Regional pricing page exists (prices vary by region); I did not retrieve it. — [Vercel regions](https://vercel.com/docs/regions)

**Cloudflare (Workers; Pages)**
- Workers Free: 100,000 requests/day, 10 ms CPU per invocation. Workers Paid: $5/month minimum per account, 10M requests and 30M CPU-ms included; overage $0.30 per extra million requests and $0.02 per extra million CPU-ms; CPU up to 5 min per invocation; cron up to 15 min CPU. About A$7.50. — [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- Static asset requests free and unlimited; no egress/bandwidth charge; subrequests not billed. — [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- Pages: 500 builds/month free, 5,000 Pro, 20,000 Business; Pages Functions count against Workers quota. The page did not say Pages is deprecated, but it points to Workers Static Assets as an alternative. — [Pages limits](https://developers.cloudflare.com/pages/platform/limits/)
- No seat charge found on the pages retrieved (not explicitly confirmed).

**Firebase (Hosting, App Hosting, Functions)**
- Spark (no cost, no payment method) vs Blaze (pay as you go). Functions and App Hosting require Blaze. — [Firebase pricing](https://firebase.google.com/pricing)
- Hosting: 10 GB storage free then $0.026/GB; 360 MB/day transfer free (about 10 GB/month) then $0.15/GB. — [Firebase pricing](https://firebase.google.com/pricing)
- App Hosting: 10 GiB/month egress free (from 1 Aug 2025), then $0.20/GiB uncached or $0.15/GiB cached; Cloud Run, Cloud Build etc. billed separately. — [Firebase pricing](https://firebase.google.com/pricing)
- Cloud Functions: 2M invocations/month free then $0.40/M; 400K GB-s and 200K CPU-s free; 5 GB outbound free then $0.12/GB. — [Firebase pricing](https://firebase.google.com/pricing)
- Firestore (Standard) free: 1 GiB, 20K writes/day, 50K reads/day. — [Firebase pricing](https://firebase.google.com/pricing)
- No seat fees found.

**AWS Amplify Hosting**
- Pay as you go, no monthly platform fee: build $0.01/min (standard), storage $0.023/GB-month, data out $0.15/GB, SSR $0.30 per 1M requests, SSR duration $0.20/GB-hour. WAF add-on $15/month per app plus WAF costs. — [Amplify pricing](https://aws.amazon.com/amplify/pricing/)
- Free tier listed (12 months): 1,000 build min, 5 GB storage, 15 GB out, 500K SSR requests, 100 GB-hours. The page also says new accounts from 15 July 2025 can get up to $200 in credits and a free plan for 6 months, which appears inconsistent with the 12-month wording; verify with AWS. — [Amplify pricing](https://aws.amazon.com/amplify/pricing/)
- Quotas: 25 apps, 5 concurrent jobs, 5 GB build artifact (new accounts are reduced). — [AWS Amplify quotas](https://docs.aws.amazon.com/general/latest/gr/amplify.html)

**Render**
- Workspace plans changed 23 April 2026: Hobby free, Pro $25/month flat (replaced $19 per member), Scale $499/month flat (replaced $29 per member), Enterprise custom. Legacy workspaces auto-moved from 1 Aug 2026. Seat fees removed; Pro and Scale have unlimited members. About A$37.50 for Pro. — [Render changelog](https://render.com/changelog/updated-plans-for-render-workspaces); [search summary of Render docs](https://render.com/docs/new-workspace-plans.md)
- Overage: $0.15/GB bandwidth, $5 per extra 1,000 build minutes, $0.25/month per extra custom domain. — [Render changelog](https://render.com/changelog/updated-plans-for-render-workspaces)
- Free web services spin down after 15 min idle (about 1 min cold start), 750 free instance hours/month, ephemeral disk. Free Postgres expires after 30 days (+14 days grace), 1 GB, no backups. Static sites are free but count toward bandwidth/build quotas. — [Render free docs](https://render.com/docs/free)
- Third-party blog (Sept 2026) says a web service starts around $7/month; not confirmed by Render's own pages. — [DevCloud blog](https://deploycloud-shopify.devcloudsoftware.com/blog/render-pricing)

**Railway**
- Free Trial ($5 one-time, 30 days), Free ($1/month credit, 1 vCPU/0.5 GB, no custom domains, 3 services), Hobby $5/month (includes $5 usage, 3 seats, 2 custom domains), Pro $20 per workspace (includes $20 usage, unlimited seats). About A$7.50 Hobby / A$30 Pro. — [Railway pricing](https://railway.com/pricing)
- Usage: memory $10/GB-month, CPU $20/vCPU-month, volumes $0.15/GB-month, egress $0.05/GB. — [Railway pricing](https://railway.com/pricing)

**Fly.io**
- No free tier for new orgs; trial is 2 hours of machine runtime or 7 days. — [Fly pricing](https://docs.fly.io/about/pricing)
- shared-cpu-1x 256 MB $2.19/month, 512 MB $3.69/month (billed per second while running); volumes $0.15/GB-month. — [Fly pricing](https://docs.fly.io/about/pricing)
- Egress $0.02/GB North America/Europe, $0.04/GB Asia Pacific/Oceania; inbound free. — [Fly pricing](https://docs.fly.io/about/pricing)
- Support: Community free, Standard $29/month, Premium $199/month. — [Fly pricing](https://docs.fly.io/about/pricing)

### Inferences
- Cheapest realistic flat-fee entry points: Cloudflare $5 (A$7.50), Railway Hobby $5, Fly about $4 to $10 (usage), Netlify Pro $20, Vercel Pro $20 plus seats, Render Pro $25 plus instance costs.
- Vercel cost grows with team size ($20 per developer); a team of 2 developers is $40 plus usage. Others are flat.
- Netlify's credit model makes bandwidth about $0.13/GB, which is lower than Vercel's $0.15/GB but both are far above Cloudflare (zero egress).

### Gaps
- Render paid instance prices (Starter/Standard), included bandwidth and build minutes for Pro: Render's pricing pages did not render in my fetch tool.
- Cloudflare seat/member charges and Firebase/Amplify team features not confirmed.
- Amplify free tier duration conflict (12 months vs 6 months) unresolved.
- Exchange rate not verified.

## 2. Commercial-use restrictions on free tiers

### Takeaway
Only Vercel Hobby is explicitly confirmed non-commercial. For Netlify, Cloudflare, Render, Railway and Fly I did not find an explicit statement either way on the pages retrieved. For a business customer portal, a free tier is risky anyway (limits, no support, spin-down, no SLA).

### Cited Findings
- Vercel Hobby: "for personal, non-commercial use"; fair-use guidelines restrict Hobby to non-commercial personal use. Pro is for professionals and businesses. — [Vercel pricing](https://vercel.com/pricing); [Vercel Hobby docs](https://vercel.com/docs/plans/hobby)
- Netlify pricing and credit docs pages do not address commercial use; terms of use not checked. — [Netlify pricing](https://www.netlify.com/pricing/)
- Cloudflare developer platform page does not state a commercial restriction; terms not retrieved. — [Cloudflare plans](https://www.cloudflare.com/plans/developer-platform/)
- Render free services: spin down after 15 minutes, suspended when 750 hours are used, can restart anytime; free Postgres expires in 30 days. Not designed for production. — [Render free docs](https://render.com/docs/free)
- Railway Free plan is $1/month credit, 1 vCPU/0.5 GB and no custom domains, so a branded portal needs Hobby ($5) or above. — [Railway pricing](https://railway.com/pricing)
- Fly.io has no ongoing free tier. — [Fly pricing](https://docs.fly.io/about/pricing)

### Inferences
- Budget for a paid plan from day one; the Cloudflare $5 plan and Railway Hobby $5 are the cheapest paid options.

### Gaps
- Explicit commercial-use terms for Netlify Free, Cloudflare Free, Firebase Spark and Amplify free tier were not verified; check each provider's Terms of Service.

## 3. Australian regions / edge, and where server code runs

### Takeaway
Sydney server/function execution is available on Vercel (syd1), Netlify (syd, Pro plan needed), Fly.io (syd), AWS Amplify (Sydney is an Amplify region; SSR region support not fully verified) and Firebase (Sydney and Melbourne function regions). Cloudflare runs Workers at the edge, including Australian cities. Render (Singapore) and Railway (Singapore) have NO Australian region.

### Cited Findings
- Vercel: 19 compute regions including syd1 (ap-southeast-2, Sydney); 126 PoPs. Functions default to iad1 (Washington DC) unless changed, so the region must be set to syd1. No Melbourne compute region listed. — [Vercel regions](https://vercel.com/docs/regions)
- Netlify: Functions regions include syd (Sydney) and sin (Singapore); default is cmh (US East Ohio). Region configuration requires a Pro or Enterprise plan. — [Netlify functions docs](https://docs.netlify.com/build/functions/optional-configuration/)
- Cloudflare: Melbourne data centre exists (NextDC M1, older press); a 2019 Cloudflare-related post lists Auckland, Brisbane, Melbourne, Perth and Sydney. A third-party tracker lists Workers in MEL as operational. No 2025/26 confirmation found. — [ITWire](https://itwire.com/business-it-news/data-centres/cloudflare-deploys-in-nextdc-melbourne-data-centre); [OpenStatus](https://www.openstatus.dev/status/cloudflare-workers/melbourne-vic-australia-mel)
- Firebase Cloud Functions: Sydney (australia-southeast1, 1st and 2nd gen) and Melbourne (australia-southeast2, 2nd gen only), both Tier 2 pricing (rates not given on that page). — [Firebase locations](https://firebase.google.com/docs/functions/locations)
- Firebase Hosting: 60-second request timeout on rewrites to functions; when region is omitted the CLI defaults to us-central1; docs recommend colocating in listed regions, none in Australia. CDN edge in Australia not stated. — [Firebase Hosting functions](https://firebase.google.com/docs/hosting/functions)
- AWS Amplify: Asia Pacific (Sydney) ap-southeast-2 is a listed Amplify region; Melbourne (ap-southeast-4) is not listed. — [AWS Amplify endpoints](https://docs.aws.amazon.com/general/latest/gr/amplify.html)
- Render regions: Oregon, Ohio, Virginia, Frankfurt, Singapore. No Australia. — [Render regions](https://render.com/docs/regions)
- Railway regions: US West, US East, EU West (Amsterdam), Southeast Asia (Singapore). No Australia. — [Railway regions](https://docs.railway.com/reference/regions)
- Fly.io: Sydney (syd) region listed, no Melbourne. Egress to Oceania $0.04/GB. — [Fly regions](https://docs.fly.io/reference/regions); [Fly pricing](https://docs.fly.io/about/pricing)

### Inferences
- Singapore-hosted Render/Railway adds roughly a cross-region round trip for Australian users; I did not find measured latency numbers (not verified).
- For Australian data residency (e.g. Privacy Act expectations), Firebase (Sydney/Melbourne), Amplify (Sydney), Fly (Sydney), Vercel (syd1) and Netlify (syd) can keep function execution in Australia, but the database must also be placed there. CDN-cached content can be served from other places.

### Gaps
- Amplify Hosting compute (SSR) Sydney support not explicitly confirmed (only that Amplify has a Sydney endpoint).
- Current Cloudflare AU PoP list and Smart Placement/region controls not verified.
- Latency measurements to Melbourne/Sydney not found.
- Whether Firebase Hosting CDN has Australian edge not stated.

## 4. Server-side code, APIs and scheduled jobs

### Takeaway
All eight can run server-side code. Scheduled jobs: Netlify (scheduled functions), Vercel (cron jobs), Cloudflare (Cron Triggers), Render (cron job service) and Railway/Fly (via a running app/machine or their cron mechanisms) are available; Firebase and Amplify typically need extra Google/AWS services.

### Cited Findings
- Netlify: sync functions (60 s), scheduled functions (30 s), background functions (15 min). — [Netlify functions docs](https://docs.netlify.com/build/functions/optional-configuration/)
- Vercel: Cron Jobs included on Hobby and Pro; function duration up to 300 s default on Pro (configurable to 800 s). Hobby cron frequency limits not retrieved. — [Vercel pricing](https://vercel.com/pricing); [Hobby docs](https://vercel.com/docs/plans/hobby)
- Cloudflare: Cron Triggers with up to 15 min CPU per invocation; example hourly cron costs about $6.99/month total. — [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- Firebase: Hosting rewrites to Cloud Functions or Cloud Run containers. Scheduled functions are not covered on the pricing page. — [Firebase Hosting functions](https://firebase.google.com/docs/hosting/functions); [Firebase pricing](https://firebase.google.com/pricing)
- Amplify Hosting compute supports Next.js 12 to 15 SSR, API routes, middleware, ISR; unsupported: edge API routes, on-demand ISR, streaming. — [Amplify SSR support](https://docs.aws.amazon.com/amplify/latest/userguide/ssr-amplify-support.html)
- Render: free tier includes Static Sites, Web Services, Postgres and Key Value; Cron Jobs listed as a service (pricing not retrieved). — [Render free docs](https://render.com/docs/free); [Render pricing](https://render.com/pricing)
- Railway and Fly run containers/VMs (always-on services, volumes); Fly machines billed per second while running. — [Railway pricing](https://railway.com/pricing); [Fly pricing](https://docs.fly.io/about/pricing)

### Inferences
- Order portal needs a database (orders, clients) and email/notifications. Netlify, Vercel, Cloudflare and Firebase offer integrated or marketplace data options; Render, Railway and Fly offer managed Postgres/volumes. I did not research database pricing in detail.

### Gaps
- Scheduled-job limits and prices for Render, Railway, Fly and Amplify not verified.
- Vercel Hobby/Pro cron frequency and count limits not retrieved.
- Cloudflare D1/KV/R2 pricing not retrieved.

## 5. Ease of use for a small non-developer team

### Takeaway
I found no authoritative independent evidence on usability. Based on feature facts only, Netlify and Vercel (Git deploy, previews, dashboards; Pro email support) and Render/Railway (dashboard-first, flat plans) look easiest; Fly.io and AWS are more engineering-heavy. Treat this as inference, not verified.

### Cited Findings
- Netlify: unlimited previews, custom domains with SSL on Free; priority email support from Personal ($9); 24/7 support only on Enterprise. — [Netlify pricing](https://www.netlify.com/pricing/)
- Vercel: Hobby has no email support; Pro has email support, spend management, viewer seats free (useful for non-developers who only view/comment). — [Vercel Hobby docs](https://vercel.com/docs/plans/hobby); [Vercel pricing](https://vercel.com/pricing)
- Fly.io: community support free, Standard $29/month, Premium $199/month. — [Fly pricing](https://docs.fly.io/about/pricing)
- Railway Free plan log history 3 days, Hobby 7, Pro 30. — [Railway pricing](https://railway.com/pricing)
- Amplify has CI/CD, branches, webhooks and (per quotas) 50 branches per app. — [AWS Amplify quotas](https://docs.aws.amazon.com/general/latest/gr/amplify.html)

### Inferences
- A non-developer team will still need a developer or agency to build the portal; hosting choice should favour whichever the developer knows. The platform dashboards matter mainly for deploy approvals, rollbacks and viewing logs.

### Gaps
- Rollback features, dashboard usability and support quality not verified from sources; no independent reviews retrieved.

## 6. Realistic monthly cost: 50-500 active clients, 200-2,000 orders/month

### Takeaway
Traffic at this scale is tiny (likely well under 50 GB/month and a few hundred thousand requests), so costs are dominated by the base plan, not usage. Estimated hosting-only range: about US$5 to $25 per month (A$8 to A$38) for Cloudflare/Railway/Fly, about $20 to $45 for Netlify/Vercel/Render, plus a database and email. These are my estimates, not provider quotes.

### Cited Findings
- Cloudflare Workers Paid $5 includes 10M requests and 30M CPU-ms, free static assets and no egress fees. — [Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- Vercel Pro $20 includes 1 TB bandwidth, 10M CDN requests and $20 usage credit; each extra developer seat $20. — [Vercel pricing](https://vercel.com/pricing)
- Netlify Pro $20 includes 3,000 credits (e.g. production deploy 15 credits, bandwidth 20 credits/GB, 2 credits per 10,000 requests). — [Netlify credit docs](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/)
- Railway Hobby $5/month includes $5 usage; one small always-on service costs about $10/GB memory and $20/vCPU per month. — [Railway pricing](https://railway.com/pricing)
- Fly: a shared-cpu-1x 512 MB machine $3.69/month plus volume $0.15/GB-month, egress $0.04/GB to Oceania. — [Fly pricing](https://docs.fly.io/about/pricing)
- Firebase: 2M function invocations/month free and 10 GB hosting transfer free, so a small portal may cost near zero beyond Blaze setup. — [Firebase pricing](https://firebase.google.com/pricing)
- Amplify: SSR 500K requests and 15 GB data out in free tier; after that $0.30 per M requests and $0.15/GB. — [Amplify pricing](https://aws.amazon.com/amplify/pricing/)

### Inferences (my own arithmetic, with stated assumptions: about 2,000 orders/month, 500 clients, perhaps 50,000 to 300,000 page/API requests/month, under 20 GB egress, 2 developers)
- Cloudflare Workers Paid: about $5 (A$8) hosting; database/email extra.
- Netlify Pro: about $20 (A$30) flat; usage unlikely to exceed 3,000 credits (20 GB is 400 credits; 300K requests is 60 credits).
- Vercel Pro: $20 (one dev) to $40 (two devs), about A$30 to A$60, plus Sydney-region function usage well inside the included credit.
- Firebase Blaze: likely $0 to $5 for hosting/functions within free quotas; database costs depend on Firestore reads/writes.
- Amplify: likely $1 to $10 after free tier; the 12-month/6-month free tier uncertainty applies.
- Render: Pro $25 plus instance(s) (probably $7+ each, unverified); about $32 to $60 (A$48 to A$90), Singapore only.
- Railway Hobby: about $5 to $15 (A$8 to A$23), Singapore only.
- Fly: about $4 to $15 (A$6 to A$23) for one or two small machines plus Postgres/volumes; Sydney available; optional $29 Standard support.
- Add: domain, transactional email, error monitoring, payment gateway fees, backups. Not researched.

### Gaps
- No real traffic data from the customer; usage figures above are assumptions.
- Database costs (Postgres/Firestore/D1) per platform not researched.
- Render instance and managed Postgres prices not verified.
- AUD figures use an assumed exchange rate.
