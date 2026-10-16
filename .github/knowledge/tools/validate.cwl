cwlVersion: v1.2
class: CommandLineTool
label: Verify GitHub evidence candidate
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONDONTWRITEBYTECODE: '1'
baseCommand: [python3, -m, evidence]
arguments:
  - validate
  - --bundle
  - $(inputs.candidate.path)
stdout: validation-report.txt
inputs:
  candidate: File
outputs:
  report:
    type: stdout
