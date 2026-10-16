cwlVersion: v1.2
class: CommandLineTool
label: Construct source-grounded workflow knowledge map
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONDONTWRITEBYTECODE: '1'
baseCommand: [python3, -m, life_science_ecosystem_lab]
arguments:
  - knowledge
  - build
  - --candidate
  - $(inputs.candidate.path)
  - --topics
  - $(inputs.topics.path)
  - --output
  - knowledge.json
inputs:
  candidate: File
  topics: File
outputs:
  knowledge:
    type: File
    outputBinding:
      glob: knowledge.json
