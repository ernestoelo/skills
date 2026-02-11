// Modified session.ts with proactive skill loading
// This shows the integration point for automatic activation

import { ProactiveLoader } from "../skill/proactive-loader" // NEW IMPORT

// ... existing session code ...

export async function handleUserMessage(message: string, session: Session) {
  // NEW: Proactive skill loading before processing
  const config = await Config.get()
  if (config.skills?.auto_activate !== false) {
    await ProactiveLoader.analyzeAndLoad(message)
  }

  // ... existing message processing ...
}

// ... rest of session code ...