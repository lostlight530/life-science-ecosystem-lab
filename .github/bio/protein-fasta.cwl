cwlVersion: v1.2
class: CommandLineTool
label: Protein FASTA composition and input-quality audit
doc: Deterministic protein FASTA validation and counts; no scientific biological inference
baseCommand: [python, -m, bio_tool, protein-fasta]
$namespaces:
  edam: http://edamontology.org/
inputs:
  fasta:
    type: File
    format: edam:format_1929
    inputBinding:
      prefix: --input
      position: 1
  output_name:
    type: string
    default: protein-fasta-report.json
    inputBinding:
      prefix: --output
      position: 2
outputs:
  report:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
