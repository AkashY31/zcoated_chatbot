# Zcoated chatbot intent library

This folder contains intent-specific reference files for a Zcoated customer-support chatbot. Use `intent-routing.md` first, then load the matching intent file. If a message covers multiple topics, answer the direct question and continue the relevant flow.

## Intent files

| Intent | File | Use for |
|---|---|---|
| Routing and shared behavior | [intent-routing.md](./intent-routing.md) | Classifying messages, shared response rules, and routing |
| Conversation end and feedback | [feedback.md](./feedback.md) | Asking for a rating at the end of a chat |
| Services | [services.md](./services.md) | Cleaning, repair, restoration, bags, and care choices |
| Pricing | [pricing.md](./pricing.md) | Published service and package prices |
| Booking and pickup | [booking-pickup-delivery.md](./booking-pickup-delivery.md) | Starting a booking or asking about pickup and delivery |
| Location and contact | [location-contact.md](./location-contact.md) | Service location, phone, email, and business hours |
| Order status | [order-status.md](./order-status.md) | Existing order, progress, or delivery status |
| Complaints and special requests | [complaints-special-requests.md](./complaints-special-requests.md) | Issues, damage concerns, special materials, or requests |
| Human support | [human-handoff.md](./human-handoff.md) | WhatsApp, phone, email, or staff escalation |
| Unknown or unsupported questions | [fallback.md](./fallback.md) | Unmatched, ambiguous, or unverified requests |

## Source and maintenance

Business facts in these files are based on the public website as checked on 2026-10-25:

- [Home](https://zcoated.com/)
- [Services](https://zcoated.com/services)
- [Pricing](https://zcoated.com/pricing)
- [Contact](https://zcoated.com/contact)

These pages may change. Verify prices, hours, service coverage, and contact details with Zcoated before launch and whenever the business updates them. Items marked **Confirm with Zcoated** are intentionally not presented as known facts.

## Integration notes

- Treat this folder as chatbot reference material, not executable code or a live booking integration.
- Use the intent names as labels if the implementation needs a classifier or routing table.
- Send the customer to the website's booking flow or a human contact channel to complete actions unless a verified booking/order integration is added.
- Do not collect payment-card details, passwords, or unnecessary personal data in chat.
- The local prototype in the project root reads these Markdown files when responding. See [the project README](../README.md) for how to run it.
