cwlVersion: v1.2
class: CommandLineTool
label: Verify GitHub evidence candidate
requirements:
  InlineJavascriptRequirement: {}
  EnvVarRequirement:
    envDef:
      PYTHONPATH: $(inputs.python_package.path)
      PYTHONDONTWRITEBYTECODE: '1'
baseCommand: [python3, -m, life_science_ecosystem_lab]
arguments:
  - evidence
  - validate
  - --bundle
  - $(inputs.candidate.path)
stdout: validation-report.txt
inputs:
  candidate: File
  python_package: Directory
outputs:
  report:
    type: stdout
