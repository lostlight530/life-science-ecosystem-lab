cwlVersion: v1.2
class: CommandLineTool
label: Construct source-grounded workflow knowledge map
requirements:
  InlineJavascriptRequirement: {}
  EnvVarRequirement:
    envDef:
      PYTHONPATH: $(inputs.python_package.path)
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
  python_package: Directory
outputs:
  knowledge:
    type: File
    outputBinding:
      glob: knowledge.json
