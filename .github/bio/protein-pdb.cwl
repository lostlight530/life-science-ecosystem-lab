cwlVersion: v1.2
class: CommandLineTool
label: Protein PDB observed C-alpha inventory audit
doc: Deterministic PDB first-model C-alpha analysis; no scientific biological inference
baseCommand: [python, -m, bio_tool, protein-pdb]
$namespaces:
  edam: http://edamontology.org/
inputs:
  pdb:
    type: File
    format: edam:format_1476
    inputBinding:
      prefix: --input
      position: 1
  output_name:
    type: string
    default: protein-pdb-report.json
    inputBinding:
      prefix: --output
      position: 2
outputs:
  report:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
