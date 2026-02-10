---
name: mcp-builder
description: Develop and scaffold MCP servers (Model Context Protocol) to integrate LLMs with external services, ensuring high-quality, extensible designs.
author: OpenCode Project Team
version: 1.1.0
---

# MCP Builder Skill Guide

## Description
The `mcp-builder` skill provides comprehensive guidelines for creating high-quality MCP servers. These servers enable LLMs to interact seamlessly with external services via Model Context Protocol (MCP). By implementing rigorous standards, tools can support real-world use cases effectively.

## When to Use the Skill
- **Building new MCP servers for APIs/services:** Ensure scalability and robust operations.
- **Designing workflows:** Optimize tool usability and discoverability for LLMs.
- **Creating server evaluations:** Develop reliable question-answer pairs to validate server performance.
- **Integrating tools with the MCP protocol:** Adopt best practices for schema design and error handling.

## Usage Guide
### MCP Server Development
#### Analyze and Plan
1. **Research Protocol:** Familiarize with the MCP specification and its core architecture.
   - Use [📋 MCP Best Practices](./references/mcp-best-practices.md) for guidelines.
2. **Select Framework:** Choose between:
   - **TypeScript**: For high compatibility and extensive SDK support.
   - **Python**: For FastAPI-based rapid development.

#### Scaffold and Implement
- **Node.js (TypeScript) Workflow**
```bash
npx mcp-node-init <server-name>
npm install
```
- **Python Workflow**
```bash
fastmcp init <server-name>
```
Set authentication, pagination, and tool input/output schemas as per the MCP requirements.

### Validation and Packaging
1. **Validate MCP Server Implementation**
   - Run `npx @modelcontextprotocol/inspector` for TypeScript.
   - For Python: Use `fastmcp validate`.
2. **Create Evaluations**
   - Refer to [✅ Evaluation Guide](./references/evaluation.md).
   - Example evaluation XML structure:
   ```xml
   <evaluation>
     <qa_pair>
       <question>What is the latest commit on repo X?</question>
       <answer>SHA12345</answer>
     </qa_pair>
   </evaluation>
   ```

## Inputs and Outputs
### Inputs
- **Framework Preference:** TypeScript or Python.
- **API Specifications:** Endpoints, authentication, and data models.

### Outputs
- **MCP Server:** Optimized for integration with LLMs.
- **Validation Results:** Passes standard validation criteria.
- **Evaluations:** XML files for server testing and refinement.

## Best Practices and Version History
### Best Practices
- Use **TypeScript SDK** for better tooling, or Python for rapid prototyping.
- Plan tool schemas carefully with descriptive names (action-oriented, e.g., `github_create_issue`).
- Implement error messages that clearly guide users.

### Version History
| Version | Date       | Updates                                                       |
|---------|------------|--------------------------------------------------------------|
| 1.1.0   | 2026-02-09 | Refined SKILL.md structure and added examples for evaluations.|
| 1.0.0   | 2025-09-18 | Initial creation based on MCP protocol standards.            |

## Resources
- [📋 MCP Best Practices](./references/mcp-best-practices.md): Core guidelines for server design.
- [✅ Evaluation Guide](./references/evaluation.md): Steps to create comprehensive evaluations.
- SDK Documentation:
  - TypeScript: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
  - Python: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`.
- Language Implementation Guides:
  - [⚡ Node/TypeScript MCP Server](./references/node-mcp-server.md).
  - [🐍 Python MCP Server](./references/python-mcp-server.md).