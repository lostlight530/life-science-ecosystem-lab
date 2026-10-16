cwlVersion: v1.2
class: CommandLineTool
label: Verify the reproducible knowledge artifact and all citations
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONDONTWRITEBYTECODE: '1'
baseCommand: [python3, -m, life_science_ecosystem_lab]
arguments:
  - knowledge
  - verify
  - --candidate
  - $(inputs.candidate.path)
  - --topics
  - $(inputs.topics.path)
  - --knowledge
  - $(inputs.knowledge.path)
stdout: knowledge-verification.txt
inputs:
  candidate: File
  topics: File
  knowledge: File
outputs:
  report:
    type: stdout
