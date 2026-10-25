const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const messages = document.querySelector("#messages");
const widget = document.querySelector("#chat-widget");
const panel = document.querySelector("#chat-panel");
const launcher = document.querySelector("#chat-launcher");
const closeButton = document.querySelector("#close-chat");
const expandButton = document.querySelector("#expand-chat");
let feedbackPrompted = false;

function setChatOpen(isOpen) {
  widget.classList.toggle("is-open", isOpen);
  panel.setAttribute("aria-hidden", String(!isOpen));
  launcher.setAttribute("aria-expanded", String(isOpen));
  launcher.setAttribute("aria-label", isOpen ? "Close Zcoated chat" : "Open Zcoated chat");
  if (!isOpen) {
    panel.classList.remove("is-expanded");
    expandButton.setAttribute("aria-label", "Expand chat");
    expandButton.title = "Expand chat";
    launcher.focus();
  } else {
    input.focus();
  }
}

function toggleExpanded() {
  const isExpanded = panel.classList.toggle("is-expanded");
  expandButton.setAttribute("aria-label", isExpanded ? "Restore chat size" : "Expand chat");
  expandButton.title = isExpanded ? "Restore chat size" : "Expand chat";
}

function addMessage(text, kind, extraClass = "", actions = []) {
  const article = document.createElement("article");
  article.className = `message ${kind}-message ${extraClass}`.trim();
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  article.append(paragraph);
  if (actions.length > 0) {
    const actionList = document.createElement("div");
    actionList.className = "message-actions";
    for (const action of actions) {
      const link = document.createElement("a");
      link.href = action.href;
      link.textContent = action.label;
      if (action.external) {
        link.target = "_blank";
        link.rel = "noreferrer";
      }
      actionList.append(link);
    }
    article.append(actionList);
  }
  messages.append(article);
  messages.scrollTop = messages.scrollHeight;
  return article;
}

function addFeedbackPrompt() {
  if (feedbackPrompted) return;
  feedbackPrompted = true;

  const prompt = addMessage(
    "How would you rate your chat experience?",
    "assistant",
    "feedback-prompt"
  );
  const options = document.createElement("div");
  options.className = "feedback-options";

  for (const rating of ["Good", "Okay", "Needs improvement"]) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = rating;
    button.addEventListener("click", () => {
      for (const option of options.querySelectorAll("button")) {
        option.disabled = true;
      }

      const feedback = `Zcoated chatbot feedback: ${rating}`;
      const whatsappUrl = `https://wa.me/918368385923?text=${encodeURIComponent(feedback)}`;
      const emailUrl = `mailto:support.zcoated@gmail.com?subject=${encodeURIComponent("Chatbot feedback")}&body=${encodeURIComponent(feedback)}`;
      addMessage(
        `Thanks for your ${rating.toLowerCase()} rating. This demo doesn't save or send ratings automatically. If you'd like to share it with Zcoated, choose WhatsApp or email.`,
        "assistant",
        "feedback-confirmation",
        [
          { href: whatsappUrl, label: "Share on WhatsApp", external: true },
          { href: emailUrl, label: "Share by email" },
        ]
      );
    });
    options.append(button);
  }

  prompt.append(options);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(text) {
  addMessage(text, "user");
  sendButton.disabled = true;
  input.disabled = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "The chatbot couldn't answer right now.");
    }
    const actions = payload.intent === "human_handoff"
      ? [
          { href: "tel:+918368385923", label: "Call Zcoated · +91 83683 85923" },
          { href: "https://wa.me/918368385923", label: "WhatsApp", external: true },
        ]
      : [];
    addMessage(payload.answer, "assistant", "", actions);
    if (payload.intent === "conversation_end") {
      addFeedbackPrompt();
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : "The chatbot couldn't answer right now.";
    addMessage(`${message} You can contact Zcoated on WhatsApp at +91 83683 85923.`, "assistant", "error-message");
  } finally {
    sendButton.disabled = false;
    input.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text || sendButton.disabled) return;
  input.value = "";
  sendMessage(text);
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    const text = button.dataset.prompt;
    if (text && !sendButton.disabled) sendMessage(text);
  });
});

launcher.addEventListener("click", () => {
  setChatOpen(!widget.classList.contains("is-open"));
});

closeButton.addEventListener("click", () => setChatOpen(false));
expandButton.addEventListener("click", toggleExpanded);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && widget.classList.contains("is-open")) {
    setChatOpen(false);
  }
});
