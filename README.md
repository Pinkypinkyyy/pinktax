# pinktax

Pink Accounting hospitality website. GitHub Pages for **pinktax.com.au**.

1. Edit the HTML (most pages are hand-maintained) or `tools/build_landing_pages.py` (the nine guide pages)
2. `python tools/build_landing_pages.py` is the rebuild. It applies `identity.json` to every page first, then builds the guide pages and the sitemap. `git status` should be clean afterwards.
3. `python -m pytest tests/ -q`
4. Push a branch. Merging to `main` publishes the site.

Business name, legal entity, office, hours, Google profile and the cross-link to the trades line all come from `identity.json`. It is generated from the firm's canonical file in `Pink-Accounting-Automation`; never edit it here.

Hospitality only. The trades line, Service Profit (a Pink Accounting service), lives on https://www.serviceprofit.com.au/ and is named on this site only in the footer cross-link and the two-doors block on /contact/.

Booking calendar: PinkAccountingTaxSolutionsClientBookings@pinktax.com.au  
Enquiry form: formsubmit to admin@pinktax.com.au

Entity: Pink Accounting & Tax Solutions Pty Ltd · ABN 51 682 301 891 · Registered Tax Agent 26284368
