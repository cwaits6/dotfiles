---
name: brainstorming
description: Collaborative ideation and exploration before implementation. Triggers when creating features, building components, adding functionality, or starting creative work. Encourages brainstorming options, discussing trade-offs, and exploring possibilities together with the user before diving into code.
---

# Brainstorming

## Purpose

This skill promotes collaborative brainstorming and creative exploration **before** jumping into implementation. It encourages Claude to think through options, discuss possibilities, and co-create solutions with users rather than immediately writing code.

## When to Use

Use this skill BEFORE starting implementation work on:

- **New features** - Exploring different approaches and design patterns
- **New components** - Discussing architecture, API design, and integration
- **Creative work** - Brainstorming solutions, evaluating alternatives, greenfield exploration
- **Functionality additions** - Considering multiple implementation paths

## Philosophy

Great software emerges from thoughtful exploration, not rushed implementation. Brainstorming means:

- 🤝 **Collaboration** - Working with the user to explore ideas together
- 💡 **Ideation** - Generating multiple options before committing to one
- 🎯 **Trade-offs** - Discussing pros/cons of different approaches
- 🗺️ **Context** - Understanding the bigger picture and constraints
- ✨ **Creativity** - Thinking beyond the obvious first solution

## Brainstorming Approaches

### 1. EnterPlanMode (For deep exploration)

Use when you need to thoroughly explore the codebase and design options:

```markdown
Let me explore the codebase and brainstorm some implementation approaches.
```

**In plan mode:**
- Discover existing patterns and conventions
- Identify multiple possible approaches
- Sketch out different architectural options
- Present trade-offs for user consideration
- Collaborate on the best path forward

### 2. AskUserQuestion (For collaborative ideation)

Use to brainstorm options and gather user preferences:

```markdown
Let me brainstorm some options with you.
```

**Discuss:**
- Different architectural approaches
- Technology/library alternatives and trade-offs
- UI/UX patterns and user experience considerations
- Performance vs simplicity trade-offs
- Integration strategies
- Future extensibility needs

### 3. Inline Exploration (For quick brainstorming)

For smaller features with a few clear options:
- Present 2-3 possible approaches
- Highlight key trade-offs
- Ask for user preference
- Confirm direction before coding

## When NOT to Brainstorm

Skip brainstorming for:

- **Bug fixes** - Clear problems with known solutions
- **Typo corrections** - Trivial text changes
- **Documentation updates** - Straightforward doc improvements
- **Simple refactoring** - Code cleanup with obvious improvements
- **Explicit specifications** - User has already done the brainstorming

## Examples

### ✅ GOOD - Collaborative Brainstorming

**User:** "Add authentication to the API"

**Claude:**
> Let me brainstorm some authentication approaches with you. I can see a few options:
>
> 1. **JWT-based auth** - Stateless, scalable, good for microservices
> 2. **Session-based auth** - Simpler, works well with SSR, easier to revoke
> 3. **OAuth2 integration** - If you need social login or third-party auth
>
> What's your use case? Do you need:
> - Social login (Google, GitHub, etc.)?
> - Just username/password?
> - Multi-device sessions?
> - Microservices architecture?

---

**User:** "Create a user dashboard component"

**Claude:**
> Before building the dashboard, let's brainstorm the approach together:
>
> **Data Architecture:**
> - Should we fetch all dashboard data at once, or load sections progressively?
> - Real-time updates needed, or static data on load?
>
> **Component Design:**
> - Single monolithic component, or composed from smaller widgets?
> - What level of customization should users have?
>
> **Integration:**
> - Should this use existing design system components?
> - Any specific layouts or grid systems you're using?
>
> Let me know your thoughts, and I'll explore the codebase to see what patterns you already have!

### ❌ BAD - Skips Brainstorming

**User:** "Add a dark mode toggle"

**Claude:**
> I'll add a dark mode toggle to your app.
> *[Immediately writes code without discussing placement, theme management strategy, persistence approach, etc.]*

**Better approach:**
> Let's brainstorm the dark mode implementation:
>
> **Approach options:**
> 1. CSS variables with data attribute toggle
> 2. Tailwind dark: class variants
> 3. CSS-in-JS theme provider
>
> **Considerations:**
> - Where should the toggle live? (Header, settings, both?)
> - Persist preference? (localStorage, user account, system preference?)
> - Sync with system dark mode setting?
>
> What fits your existing setup best?

## Brainstorming Flow

```
User requests new feature/component
         |
         v
Is this a bug fix or trivial change?
         |
    No   |   Yes → Proceed directly
         v
Present 2-3 possible approaches
         |
         v
Discuss trade-offs and constraints
         |
         v
User provides preference/guidance
         |
         v
Complex? → EnterPlanMode for deep dive
Simple? → Quick confirmation and proceed
```

## Integration with Tools

This skill leverages:

- **EnterPlanMode** - Deep exploration and multi-option design
- **AskUserQuestion** - Collaborative option discussion
- **TodoWrite** - Organizing implementation after alignment

## Brainstorming Best Practices

### DO:
✅ Present multiple viable options
✅ Explain trade-offs clearly
✅ Ask about constraints and preferences
✅ Consider future extensibility
✅ Explore the codebase to understand patterns
✅ Think beyond the first obvious solution

### DON'T:
❌ Present only one option as "the way"
❌ Make technology choices without discussion
❌ Ignore existing codebase patterns
❌ Jump to code before alignment
❌ Over-engineer with unnecessary options
❌ Paralyze with too many choices (2-4 options is ideal)

## Effective Brainstorming Questions

### For Features:
- What's the core user need we're solving?
- What's the simplest version that would work?
- What future extensions might we need?
- What are the performance/security implications?

### For Components:
- How will this fit into the existing component hierarchy?
- What props/API would make this most reusable?
- Should this be a controlled or uncontrolled component?
- What edge cases or states need handling?

### For Architecture:
- What patterns are we already using?
- What scale are we designing for?
- What's the maintenance burden of each option?
- How does this integrate with our deployment setup?

## Measuring Success

Brainstorming is effective when:
- ✅ Users feel like active collaborators, not just requesters
- ✅ Multiple options are considered, not just the first idea
- ✅ Decisions are made with clear understanding of trade-offs
- ✅ Implementation matches user's actual needs and constraints
- ✅ Solutions are well-suited to the existing codebase

## Common Brainstorming Patterns

### Pattern 1: The Three Options

Present three levels of implementation:
- **Minimal** - Simplest solution, fastest to implement
- **Standard** - Balanced approach with good extensibility
- **Comprehensive** - Full-featured with all edge cases

### Pattern 2: The Trade-Off Matrix

Compare options across key dimensions:
- Complexity vs Features
- Performance vs Developer Experience
- Flexibility vs Simplicity
- Immediate needs vs Future extensibility

### Pattern 3: The Discovery Session

For unclear requirements:
1. Explore codebase to understand context
2. Present what you found
3. Propose 2-3 directions based on discoveries
4. Collaborate on the best fit

## Related Skills

- **EnterPlanMode** - Deep planning and exploration
- **AskUserQuestion** - Collaborative decision making
- **TodoWrite** - Organizing work after brainstorming

---

**Remember:** The best code comes from collaborative thinking, not solo assumptions. Brainstorm first, implement second. 🧠✨
