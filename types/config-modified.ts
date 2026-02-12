// Modified config.ts with auto_activate option
// This shows the changes needed for the OpenCode PR

// ... existing imports ...

export const Config = z.object({
  // ... existing fields ...

  skills: z.object({
    paths: z.array(z.string()).optional(),
    urls: z.array(z.string()).optional(),
    auto_activate: z.boolean().default(true), // NEW: Enable automatic skill activation
  }).optional(),

  // ... rest of config ...
})

// ... existing code ...

export namespace Config {
  // ... existing code ...

  // Modified directories function to include workflows/skills path
  export async function directories(): Promise<string[]> {
    const config = await get()
    const dirs = [
      path.join(Global.Path.home, ".opencode"),
      // NEW: Add workflows/skills path for automatic loading
      path.join(Global.Path.home, ".copilot", "workflows", "skills"),
    ]

    // ... rest of function ...
  }
}