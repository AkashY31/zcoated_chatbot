# Zcoated chatbot MVP

A small, local website chatbot that uses the Markdown intent references in [`intents/`](./intents/) to answer common Zcoated questions. It uses deterministic intent routing and response templates; it does not call an AI service, need an API key, create bookings, or look up live order status.

The demo page uses a dark, warm-gold premium visual style inspired by Zcoated's public website. The chatbot appears as a floating launcher in the bottom-right corner; users can open the chat panel, expand it, restore it, or close it. This project is a standalone preview, not a deployment or modification of the live zcoated.com website. To place the widget on the real site, its owner needs to integrate these files with the website source and deploy that change.

## Requirements

- Python 3.10 or later
- No third-party Python packages

## Run locally

From this folder, run:

```powershell
python app.py
```

Then open [http://127.0.0.1:8765](http://127.0.0.1:8765). Stop the server with `Ctrl+C`.

## Run tests

```powershell
python -m unittest discover -s tests
```

## How the intent files are used

The server routes a question to an intent and reads the matching Markdown file from `intents/` when generating a response. Contact details, service descriptions, and prices are taken from those files. If the files are updated, restart the server only if the change affects Python response logic; Markdown facts are read from disk on each message.

## MVP scope and next steps

- Covers service information, published pricing, pickup guidance, location/contact details, order-status limitations, complaints, human handoff, and fallback.
- Uses a lightweight keyword router; this is a prototype and may misclassify unfamiliar phrasing.
- Booking requests are handed to the Zcoated contact channel; no booking is created by the app.
- Order progress is not connected to a live order system.
- On clear conversation endings (for example, “bye” or “that's all”), the bot asks for a rating. Ratings are not stored by this demo; customers can explicitly share their selection through a pre-filled WhatsApp or email link.
- Before a public launch, confirm the intent content with Zcoated and add a production backend, abuse protection, privacy notice, monitoring, and any approved booking/order integrations.
