# Assignment 2 Reflection

**Name:** [Your name]
**Option:** [A/B - Calendar/Tasks]
**Date:** [Submission date]

---

## Tool Design Decisions

### Tools Implemented
1. **[tool_name]**: [Brief description of what it does]
2. **[tool_name]**: [Brief description]
3. **[tool_name]**: [Brief description]

### Why These Tools?
[Explain why you chose to implement these specific tools. What user needs do they address?]

### Description Strategy
[How did you write your tool descriptions to help the LLM select the right tool? What keywords or patterns did you use?]

---

## Challenges Encountered

### Challenge 1: [Name]
- **Problem:** [What went wrong or was difficult]
- **Solution:** [How you solved it]

### Challenge 2: [Name]
- **Problem:** [What went wrong]
- **Solution:** [How you solved it]

---

## Error Handling Approach

[Describe your approach to error handling. What types of errors did you anticipate? How do you communicate errors to users?]

---

## Bonus: Token Comparison

Only if you did the bonus. Measure, don't estimate: use `event.usage_metadata.prompt_token_count` or Gemini `countTokens` (see the README section "Bonus: Tool Search Pattern"). Run both agents on the same query.

| Mode | ADK version | Model | Query | First-call prompt tokens | Whole-turn prompt tokens |
|------|-------------|-------|-------|--------------------------|--------------------------|
| All GitHub tools (`create_agent()`) | | | | | |
| Tool search (`create_agent_with_tool_search()`) | | | | | |

- **Measured with:** [usage_metadata / countTokens]
- **Reduction:** first call [ ]%, whole turn [ ]%
- **One limit you noticed:** [e.g. what the search costs, or what changes with the ADK version]

---

## Ideas for Improvement

If you had more time, what would you add or change?

1. [Improvement idea]
2. [Improvement idea]
3. [Improvement idea]

---

## Key Learnings

What did you learn from this assignment about building AI agents?

[Your reflection here - 2-3 paragraphs]
