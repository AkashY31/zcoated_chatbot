# Intent: booking, pickup, and delivery

## Match this intent when

The customer wants to book a service, arrange pickup, ask how collection works, or confirm whether pickup and return delivery are available.

## Example messages

- “I want to book a shoe cleaning.”
- “Can you pick up from my home?”
- “Is pickup and delivery free?”
- “How do I schedule a pickup?”
- “Can I book for tomorrow?”
- “Do you collect from my area?”

## Confirmed information

- Zcoated advertises free pickup and delivery at the customer's doorstep in Gurgaon.
- The website describes a process of booking, doorstep pickup, professional cleaning/repair, and return delivery.
- The website asks customers to contact Zcoated for pickup support and scheduling.
- Public contact options are listed in [human-handoff.md](./human-handoff.md).

## Booking behavior

1. Ask which service the customer wants and how many items they have, if not already stated.
2. Ask for their Gurgaon locality or PIN code only if needed to check service coverage.
3. If an operational booking integration exists, create the booking only after receiving its successful confirmation.
4. Otherwise, provide the website's booking path or hand off to Zcoated using WhatsApp or phone. Do not claim the booking is complete.
5. Ask about preferred pickup date/time only if a real scheduling channel can confirm availability.

## Response guidance

- You may say pickup and delivery are advertised as free in Gurgaon.
- Do not confirm coverage for a particular address, pickup slot, same-day service, collection time, or service outside Gurgaon unless a live source or staff confirms it.
- Do not invent turnaround or delivery estimates. See [order-status.md](./order-status.md).
- For prices, use [pricing.md](./pricing.md).

## Example response

> Zcoated advertises free doorstep pickup and delivery in Gurgaon. Please share your locality or PIN code and the service you need; the team can confirm coverage and arrange a pickup. You can contact them on WhatsApp at +91 83683 85923.

## Not confirmed

Exact pin-code coverage, scheduling availability, booking form behavior, pickup windows, turnaround time, and booking cancellation/change procedures are not specified in the public information reviewed. Confirm these with Zcoated before stating them as policy.
