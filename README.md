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

### As this repo

```bash
uv sync
```

### As a dependency of another project (path / git)

```bash
uv add /path/to/structure_tools
# or: uv add git+ssh://.../structure_tools
```

`structure_tools` depends on plain PyPI `torch` so this works on macOS (MPS/CPU) and Linux. CUDA is **not** pinned in the library metadata on purpose — a `cu128` source here would break Mac consumers.

### GPU / CUDA 12.8 (H200, Linux only)

CUDA wheels do not exist for macOS. On a Linux GPU host or in Docker:

```bash
UV_TORCH_BACKEND=cu128 uv sync
```

Or build/run the included Dockerfile (`nvidia/cuda:12.8...`), which sets `UV_TORCH_BACKEND=cu128` for you. Never export that variable on a Mac.


