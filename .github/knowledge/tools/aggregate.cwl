cwlVersion: v1.2
class: CommandLineTool
label: Aggregate GitHub evidence
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONDONTWRITEBYTECODE: '1'
baseCommand: [python3, -m, evidence]
arguments:
  - aggregate
  - --input
  - $(inputs.records.path)
  - --topics
  - $(inputs.topics.path)
  - --output
  - candidate.json
inputs:
  records: File
  topics: File
outputs:
  candidate:
    type: File
    outputBinding:
      glob: candidate.json
