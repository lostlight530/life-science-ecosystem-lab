cwlVersion: v1.2
class: CommandLineTool
label: Aggregate GitHub evidence
requirements:
  InlineJavascriptRequirement: {}
  EnvVarRequirement:
    envDef:
      PYTHONPATH: $(inputs.python_package.path)/.github/runtime:$(inputs.python_package.path)
      PYTHONDONTWRITEBYTECODE: '1'
baseCommand: [python3, -m, life_science_ecosystem_lab]
arguments:
  - evidence
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
  python_package: Directory
outputs:
  candidate:
    type: File
    outputBinding:
      glob: candidate.json
