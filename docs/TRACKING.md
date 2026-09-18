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
- Meta pixel `26989404134047568` (Events Manager dataset "Pink Document Capture")
- Meta Conversions API is not installed: this site is static GitHub Pages and has no server. Email and phone are SHA-256 hashed in the browser before they are offered to the pixel.

## Lead relay

Forms POST through `https://formsubmit.co/ajax/admin@pinktax.com.au`. FormSubmit is **per-origin**. `pinktax.com.au` has to be activated from a live-domain submission (an activation mail to admin@). If the relay returns `success: "false"`, the page does not thank the visitor or fire a conversion; it opens a mailto fallback instead.

## After each deploy

1. Submit the contact form and the Margin Check lead form from https://pinktax.com.au (not localhost).
2. Confirm the mail arrives at admin@pinktax.com.au.
3. Click Book → Pick a time and confirm GA4 realtime shows `book_click`.
4. Click the phone number and confirm `phone_click`.
5. In GA4, mark `generate_lead`, `book_click` and `phone_click` as key events, then import them into Google Ads.
