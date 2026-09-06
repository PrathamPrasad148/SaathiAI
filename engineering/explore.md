# Explore Agent

Read-only search agent for broad fan-out searches — when answering means sweeping many files, directories, or naming conventions and you only need the conclusion, not the file dumps. It reads excerpts rather than whole files, so it locates code; it doesn't review or audit it.

**Specify search breadth:** "medium" for moderate exploration, "very thorough" for multiple locations and naming conventions.

**Tools:** All tools except Agent, Artifact, ArtifactComments, ArtifactData, ArtifactCheck, ExitPlanMode, Edit, Write, NotebookEdit

This agent is ideal for:
- Finding all files matching a pattern or naming convention
- Searching across multiple directories for related code
- Locating specific functions, classes, or patterns
- Getting an overview of how something is implemented across the codebase
- Without needing to review or audit the found code