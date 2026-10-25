# Intent: fallback and unsupported questions

## Match this intent when

The message does not match another intent, is too ambiguous to answer safely, or asks for information not present in the approved references.

## Response behavior

- If the request is ambiguous, ask one concise clarifying question. Offer likely topics such as services, prices, booking/pickup, or order status.
- If the question is clear but the answer is not known, say so plainly and offer human handoff.
- Do not fabricate details, guess policies, or turn an unverified assumption into a fact.
- For unrelated questions, politely explain that you can help with Zcoated services and contact options.
- For urgent complaints or a request for a person, use [human-handoff.md](./human-handoff.md).

## Example responses

**Ambiguous**

> Are you looking for service details, pricing, or help arranging a pickup?

**Not confirmed**

> I don't have confirmed information about that. The Zcoated team can help at +91 83683 85923 or support.zcoated@gmail.com.

**Outside scope**

> I can help with Zcoated's shoe and bag care services, pricing, and pickup information. What would you like to know?
