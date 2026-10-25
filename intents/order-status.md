# Intent: order status and turnaround

## Match this intent when

The customer asks about an existing order, current repair/cleaning progress, expected completion, return delivery, or delay.

## Example messages

- “What is the status of my shoes?”
- “When will I get my shoes back?”
- “Has my order been picked up?”
- “Is my repair ready?”
- “My delivery is late.”

## Available information

The public website describes pickup, expert care, and return delivery, and mentions live support. It does not publish a public order-tracking method or a standard turnaround time.

## Response behavior

- If an authenticated order-management integration is available, use it and report only the result it returns.
- Otherwise, do not claim to look up an order or estimate a completion/delivery date.
- Offer to connect the customer with Zcoated through [human-handoff.md](./human-handoff.md).
- For handoff, ask for an order/reference number only if the customer has one and the contact channel needs it. Avoid collecting sensitive information.
- If the customer reports a delay or lost item, acknowledge the concern and prioritize staff handoff.

## Example response

> I can’t see live order progress here, and Zcoated does not publish a standard turnaround time. Please WhatsApp the team at +91 83683 85923 with your order/reference number, if available, so they can check it for you.

## Do not

- Invent a turnaround time or claim the order is on schedule.
- Say an item has been collected, completed, or dispatched without a verified system response.
- Ask for payment credentials or account passwords.
