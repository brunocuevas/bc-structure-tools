import logging
import os

import click
from logging import Logger

from structure_tools.wrappers import parse_json_input, input_validation, build_structure_input

l = Logger("main logger", level=logging.INFO)

DEFAULT_NUM_LOOPS = 20
DEFAULT_NUM_SAMPLING_STEPS = 100
DEFAULT_NUM_DIFFUSION_SAMPLES = 1
DEFAULT_SEED = 0


def load_model():
    from esm.models.esmfold2 import EsmFold2Model

    model = EsmFold2Model.from_pretrained(
        "biohub/ESMFold2",
        device="cuda",
    ).eval()
    return model


def fold_option(name, default, help_text):
    return click.option(name, default=default, show_default=True, type=int, help=help_text)


def common_fold_options(fn):
    fn = fold_option("--num-loops", DEFAULT_NUM_LOOPS, "Number of folding loops.")(fn)
    fn = fold_option(
        "--num-sampling-steps",
        DEFAULT_NUM_SAMPLING_STEPS,
        "Number of diffusion sampling steps.",
    )(fn)
    fn = fold_option(
        "--num-diffusion-samples",
        DEFAULT_NUM_DIFFUSION_SAMPLES,
        "Number of diffusion samples.",
    )(fn)
    fn = fold_option("--seed", DEFAULT_SEED, "Random seed for folding.")(fn)
    return fn


@click.group()
def cli():
    pass


def _load_and_validate(input_file):
    input_content = parse_json_input(input_file)
    l.info(f"Preparing for prediction of {len(input_content)} entries")

    validated_content = []
    for i, item in enumerate(input_content):
        try:
            input_validation(item)
            validated_content.append(item)
        except IOError:
            l.error(f"Unable to validate entry {i}")

    l.info(f"Validation completed, ready for {len(validated_content)} entries")
    return validated_content


def _write_fold_result(name, result):
    """Write one or more mmCIF outputs from a fold result."""
    results = result if isinstance(result, list) else [result]
    for i, sample in enumerate(results):
        suffix = "" if len(results) == 1 else f".sample{i}"
        out_path = f"{name}{suffix}.esmfold2.cif"
        with open(out_path, "w") as f:
            f.write(sample.complex.to_mmcif())
        l.info(f"Wrote {out_path}")


@cli.command()
@click.argument("INPUT_FILE")
@common_fold_options
def local_prediction(
    input_file,
    num_loops,
    num_sampling_steps,
    num_diffusion_samples,
    seed,
):
    from esm.models.esmfold2 import ESMFold2InputBuilder

    validated_content = _load_and_validate(input_file)

    l.info("Loading model")
    model = load_model()
    l.info("Finished loading model")

    for item in validated_content:
        spi = build_structure_input(item)
        result = ESMFold2InputBuilder().fold(
            model,
            spi,
            num_loops=num_loops,
            num_sampling_steps=num_sampling_steps,
            num_diffusion_samples=num_diffusion_samples,
            seed=seed,
        )
        _write_fold_result(item["name"], result)


@cli.command()
@click.argument("INPUT_FILE")
@common_fold_options
def remote_prediction(
    input_file,
    num_loops,
    num_sampling_steps,
    num_diffusion_samples,
    seed,
):
    from esm.sdk.api import FoldingConfig
    from esm.sdk.forge import SequenceStructureForgeInferenceClient

    validated_content = _load_and_validate(input_file)

    # FoldingConfig currently exposes loops/steps only; keep the shared CLI
    # knobs and warn when remote-unsupported values are non-default.
    if num_diffusion_samples != DEFAULT_NUM_DIFFUSION_SAMPLES:
        l.warning(
            "num_diffusion_samples=%s is not supported by remote FoldingConfig; ignoring",
            num_diffusion_samples,
        )
    if seed != DEFAULT_SEED:
        l.warning(
            "seed=%s is not supported by remote FoldingConfig; ignoring",
            seed,
        )

    config = FoldingConfig(num_loops=num_loops, num_sampling_steps=num_sampling_steps)
    token = os.environ.get("BIOHUB_TOKEN") or os.environ.get("BIOHUB_TOKKEN")
    if not token:
        raise click.ClickException(
            "Set BIOHUB_TOKEN in the environment for remote prediction."
        )
    client = SequenceStructureForgeInferenceClient(
        model="esmfold2-fast-2026-05",
        url="https://biohub.ai",
        token=token,
    )

    for item in validated_content:
        spi = build_structure_input(item)
        result = client.fold_all_atom(spi, config=config)
        if not (isinstance(result, list) or hasattr(result, "complex")):
            raise click.ClickException(
                f"Remote fold failed for {item['name']}: {result}"
            )
        _write_fold_result(item["name"], result)
