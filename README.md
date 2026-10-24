# Structure tools 

## Why?

Providing a convenient set of tools and scripts to work on protein structures, including protein structure prediction, analysis and simulation

## Content 


### Protein Structure prediction

#### ESMFold2

Two options: 

- **Remote prediction**. Requires adding a biohub token to BIOHUB_TOKEN 
- **Local prediction**. Requires having storage and a GPU

The script is aimed to taken JSON files following exactly the same format spec than AF3, except that more than one input are boundled on a top level list. 

Example:

```bash

uv run esm2 remote-prediction example.1.json

```

Where `example.1.json` is:


```
[
  {
    "name": "system1",
    "sequences": [
        [
          "protein",
          {
            "id": ["A"],
            "sequence": "MSPQTETKASVGFKAGVKEYKLTYYTPEYETKDTDILAAFRVTPQPGVPPEEAGAAVAAESSTGTWTTVWTDGLTSLDRYKGRCYHIEPVPGEETQFIAYVAYPLDLFEEGSVTNMFTSIVGNVFGFKALAALRLEDLRIPPAYTKTFQGPPHGIQVERDKLNKYGRPLLGCTIKPKLGLSAKNYGRAVYECLRGGLDFTKDDENVNSQPFMRWRDRFLFCAEAIYKSQAETGEIKGHYLNATAGTCEEMIKRAVFARELGVPIVMHDYLTGGFTANTSLSHYCRDNGLLLHIHRAMHAVIDRQKNHGMHFRVLAKALRLSGGDHIHAGTVVGKLEGDRESTLGFVDLLRDDYVEKDRSRGIFFTQDWVSLPGVLPVASGGIHVWHMPALTEIFGDDSVLQFGGGTLGHPWGNAPGAVANRVALEACVQARNEGRDLAVEGNEIIREACKWSPELAAACEVWKEITFNFPTIDKLDGQE"
          }
        ],
        [
          "protein",
          {
            "id": ["D"],
            "sequence": "MASSMLSSAAVVTSPAQATMVAPFTGLKSSAAFPVTRKTNKDITSIASNGGRVSCMKVWPPIGKKKFETLSYLPDLSDVELAKEVDYLLRNKWIPCVEFELEHGFVYREHGNTPGYYDGRYWTMWKLPLFGCTDSAQVLKEVEECKKEYPGAFIRIIGFDNTRQVQCISFIAYKPPSFTEA"
          }
        ],
        [
          "ligand",
          {
            "id": ["E", "F"],
            "ccd": "MG"
          }
        ]
    ],
    "version": "1",
    "dialect": "alphafold3"
  }
]
```

## Installation

Clone, uv sync. 


