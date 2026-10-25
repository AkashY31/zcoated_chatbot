# Intent: conversation end and feedback

## Match this intent when

The customer clearly ends the conversation, for example: “bye”, “goodbye”, “thank you”, “that's all”, or “nothing else”.

Do not trigger just because a message contains “thanks” if the customer also asks a new question.

## Response behavior

- Say a brief, friendly goodbye.
- Ask the customer to rate their chat experience.
- Offer the options **Good**, **Okay**, and **Needs improvement**.
- In the local MVP, ratings are not stored or sent automatically. Be transparent about this.
- After a rating, offer a pre-filled WhatsApp or email link so the customer can explicitly share feedback with Zcoated.
- Do not claim that feedback has been submitted or recorded unless a feedback backend confirms it.

## Example

> Thanks for chatting with Zcoated! Before you go, how was your experience?

## Privacy and implementation

Only open an external WhatsApp or email message after the customer chooses to share feedback. Do not send feedback automatically.
