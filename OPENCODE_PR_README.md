# OpenCode Proactive Skill Loader Integration

This PR adds automatic skill activation functionality to OpenCode, allowing skills to be activated automatically based on conversation context without manual @ mentions.

## Overview

The proactive skill loader analyzes user messages and automatically activates relevant skills based on keyword patterns. This improves user experience by reducing manual skill activation while maintaining precise control over when skills are loaded.

## Files Changed

### New Files
- `src/types/proactive-loader.ts` - Core proactive loading logic with pattern matching
- `src/types/config-modified.ts` - Configuration updates for auto-activation settings

### Modified Files
- `src/types/skill.ts` - Integration point for automatic loading (see skill-modified.ts)
- `src/types/session.ts` - Session handling for proactive activation (see session-modified.ts)

## Key Features

- **Automatic Pattern Matching**: Uses regex patterns to detect skill activation keywords
- **Multi-language Support**: Includes Spanish and English patterns for better accessibility
- **Configurable**: Can be disabled via config setting `skills.auto_activate`
- **Non-intrusive**: Only activates when patterns are clearly matched
- **Performance Optimized**: Uses efficient regex matching with early termination

## Supported Skills & Patterns

| Skill | English Patterns | Spanish Patterns |
|-------|------------------|------------------|
| architect | scaffold, create skill, template | - |
| dev-workflow | git commit, push pull, merge | hacer commit en git |
| pdf | pdf process, extract text | procesar PDF con texto |
| web-scraper | scrape web, web crawler | - |
| sys-env | system environment, arch linux | instalar paquete Arch Linux |
| code-review | code review, security | revisar código Python |
| recursive-context | recursive context, large input | - |
| mcp-builder | mcp server, model context protocol | construir servidor MCP |

## Configuration

Add to OpenCode config:
```typescript
{
  skills: {
    auto_activate: true,  // Enable/disable automatic activation
    paths: ["~/.copilot/workflows/skills"],  // Additional skill paths
    urls: []  // Remote skill sources
  }
}
```

## Testing

The implementation includes comprehensive testing covering:
- Keyword analysis with multiple languages
- Edge cases (empty messages, multiple skills)
- Pattern matching accuracy
- Performance with large messages

## Backwards Compatibility

- Existing manual @ skill activation continues to work
- New feature is opt-in via configuration
- No breaking changes to existing APIs
- Skills can still be loaded manually when needed

## Usage Examples

**Automatic activation:**
```
User: "Necesito hacer commit en git y revisar código Python"
→ Automatically activates: dev-workflow, code-review
```

**Manual override still works:**
```
User: "@architect create new skill"
→ Explicitly loads architect skill
```

## Implementation Details

The proactive loader integrates at the session level, analyzing messages before processing and injecting relevant skills into the context. Pattern matching uses case-insensitive regex with early termination for performance.

## Future Enhancements

- Machine learning-based pattern recognition
- User feedback loop for pattern accuracy
- Custom pattern configuration per user
- Integration with conversation history for context awareness