# Site tracking (pinktax.com.au)

Required by `Pink - web and tracking change brief.docx` (18 September 2026) before paid spend scales.

## What fires

| Action | GA4 event | Meta |
|--------|-----------|------|
| Margin Check enquiry (name, email, phone) | `generate_lead` (`lead_source: margin_check`) | `Lead` |
| Contact form | `generate_lead` (`lead_source: contact_form`) | `Lead` |
| Book calendar click | `book_click` (`lead_source: outlook_booking`) | `Lead` |
| Phone click | `phone_click` | `Contact` |
| Page load | GA4 page_view | `PageView` |

`generate_lead` is not fired on a calendar click or on the calculator itself. A lead is a person who left contact details, or a phone click, or an intent-to-book click.

Venue takings, wages and rent stay in the browser. The relay only sends name, email, phone, venue and message.

## Tags

- GA4 `G-8T6SXPNSCW` via gtag.js
- Google tag `GT-WVXQ29L2`
- Google Ads `AW-` conversion id is empty until the Ads account supplies it. Do not invent one.
- Meta pixel `1237708438188688` ("Pink Accounting's Pixel", the dataset attached to ad account 543906261707152). The earlier id `26989404134047568` was changed on 18 Sep 2026 and must not be restored; the comment in `track.js` has the reason.
- Meta Conversions API is not installed: this site is static GitHub Pages and has no server. Email and phone are SHA-256 hashed in the browser before they are offered to the pixel.

## Lead relay

Forms POST through `https://formsubmit.co/ajax/admin@pinktax.com.au`. FormSubmit is **per-origin**. `pinktax.com.au` has to be activated from a live-domain submission (an activation mail to admin@). If the relay returns `success: "false"`, the page does not thank the visitor or fire a conversion; it opens a mailto fallback instead.

## After each deploy

1. Submit the contact form and the Margin Check lead form from https://pinktax.com.au (not localhost).
2. Confirm the mail arrives at admin@pinktax.com.au.
3. Click Book → Pick a time and confirm GA4 realtime shows `book_click`.
4. Click the phone number and confirm `phone_click`.
5. In GA4, mark `generate_lead`, `book_click` and `phone_click` as key events, then import them into Google Ads.

## Ready-to-enable placement (nothing below is live)

None of these ids exist in the repo yet. Do not invent them; each needs an owner with a sign-in.

- **Search Console.** Preferred: DNS TXT verification at the domain host (a `google-site-verification` TXT record already exists on the apex, set up by whoever verified it first, so check who owns that property before adding another). If an HTML-tag method is chosen instead, the tag is one `<meta name="google-site-verification" content="...">` in `<head>` of `index.html` only, and the content value comes from the Search Console property owner.
- **Google Tag Manager.** Not installed and not needed while `track.js` loads GA4 and the Google tag. Adding GTM alongside would double-count; decide one or the other.
- **Google Ads (AW-).** `AW` in `track.js` is empty on purpose. Fill it, and the conversion label, only from the Ads account.
- **Lead source on enquiries.** `nav.js` can add UTM, click id, landing path and referrer host to the enquiry post once `ATTRIBUTION_ENABLED` is set to true (branch `seo/lead-source-capture-2026-10-25`). Turn it on only after the privacy policy discloses it.
