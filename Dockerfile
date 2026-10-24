# GPU image for the structure_tools `esm2` CLI (ESMFold2 local_prediction).
# Requires NVIDIA Container Toolkit on the host:
#   docker run --gpus all -v "$PWD:/data" -v esm2-models:/models structure-tools-esm2 \
#     local_prediction /data/input.json
FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1 \
    # Prefer CUDA wheels when resolving torch (matches torch 2.11 + CUDA 12.8).
    UV_TORCH_BACKEND=cu128 \
    # Persist HF / torch downloads across runs via a mounted volume.
    HF_HOME=/models \
    HUGGINGFACE_HUB_CACHE=/models/hub \
    TRANSFORMERS_CACHE=/models/transformers \
    TORCH_HOME=/models/torch \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        python3.12 \
        python3.12-venv \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.12 /usr/local/bin/python \
    && ln -sf /usr/bin/python3.12 /usr/local/bin/python3

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Dependency layer first for better cache reuse.
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv venv /opt/venv \
    && uv sync --python /opt/venv/bin/python --frozen --no-dev \
    && /opt/venv/bin/python -c "import torch; assert torch.version.cuda, 'CPU-only torch installed'; print('torch', torch.__version__, 'cuda', torch.version.cuda)"

ENV PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV=/opt/venv

RUN mkdir -p /data /models /outputs \
    && chmod 777 /data /models /outputs

WORKDIR /data

# Default entrypoint is the project console script from pyproject.toml.
ENTRYPOINT ["esm2"]
CMD ["--help"]
