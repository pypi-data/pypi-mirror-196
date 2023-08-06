# Stateless MSB API
# Version of API functions that don't require a sketchbook object

from PIL import Image
import requests
from io import BytesIO
import math
from .helper_functions import *

# MSB IMPORTS ================================
import sys

sys.path.append("..")
import model_sketch_book as msb
from Concept import (
    get_prompt,
    get_gpt_response,
    calc_max_example_length,
    image_text_similarity,
)
from msb_enums import InputType, OutputType, SketchMode, idMode, ModelType

# Set up CLIP ================================
import open_clip

# Load model and preprocess function
CLIP_MODEL, _, CLIP_PREPROCESS = open_clip.create_model_and_transforms(
    "ViT-B-32-quickgelu", pretrained="laion400m_e32"
)


def concept_fn(
    x,
    concept_term: str,
    input_type: InputType,
    debug: bool = False,
):
    if input_type == InputType.Image or input_type == InputType.ImageLocal:
        return get_img_concept_pred(x, concept_term, input_type, debug)
    elif input_type == InputType.Text:
        return get_text_concept_pred(x, concept_term, debug)
    else:
        raise Exception(f"Input type {input_type} not supported.")


def concept_fn_batch(
    x_arr,
    concept_term: str,
    input_type: InputType,
    debug: bool = False,
):
    if input_type == InputType.Image or input_type == InputType.ImageLocal:
        return get_img_concept_pred_batch(x_arr, concept_term, input_type, debug)
    elif input_type == InputType.Text:
        return get_text_concept_pred_batch(x_arr, concept_term, debug)
    else:
        raise Exception(f"Input type {input_type} not supported.")


# Returns a binary prediction for the provided concept term on the provided example x. The example must be a string (text).
def get_text_concept_pred(
    x, concept_term, debug, model="text-davinci-002", max_tokens=200
):
    # Formulate prompt
    max_example_length = calc_max_example_length(
        max_tokens=max_tokens,
        chunk_size=1,
    )
    prompt = get_prompt(
        x_arr=[x],
        concept_term=concept_term,
        max_example_length=max_example_length,
    )
    if debug:
        print("prompt", prompt)

    # Get prediction
    pred_arr, res_arr = get_gpt_response(
        model=model,
        cur_prompt=prompt,
        max_tokens=max_tokens,
        concept_term=concept_term,
        is_batched=False,
    )
    pred = pred_arr[0]

    if debug:
        print(f"res_arr: {res_arr}, pred: {pred}")
    return pred


# Returns a binary prediction for the provided concept term on the provided example x. The example must be a string (text).
def get_text_concept_pred_batch(
    x_arr,
    concept_term,
    debug,
    model="text-davinci-002",
    chunk_size=10,
    max_tokens=200,
    min_chunk_size=1,
):
    n_examples = len(x_arr)
    chunk_sizes_to_try = msb.generate_chunk_sizes(
        chunk_sizes_to_try=[], min_chunk_size=min_chunk_size, chunk_size=chunk_size
    )

    for chunk_size_to_try in chunk_sizes_to_try:
        chunk_size = chunk_size_to_try
        n_chunks = math.ceil(n_examples / chunk_size)
        max_example_length = calc_max_example_length(max_tokens, chunk_size)
        full_pred_arr = []
        for i in range(n_chunks):
            start_i = int(i * chunk_size)
            end_i = min(int(start_i + chunk_size), n_examples)
            cur_x_arr = x_arr[start_i:end_i]

            # Formulate prompt
            prompt = get_prompt(
                x_arr=cur_x_arr,
                concept_term=concept_term,
                max_example_length=max_example_length,
            )
            if debug:
                print("prompt", prompt)

            # Get prediction
            pred_arr, res_arr = get_gpt_response(
                model=model,
                cur_prompt=prompt,
                max_tokens=max_tokens,
                concept_term=concept_term,
                is_batched=True,
            )
            full_pred_arr.extend(pred_arr)

            if debug:
                print(f"Chunk {i}, res_arr: {res_arr}, pred_arr: {pred_arr}")

        if len(full_pred_arr) == n_examples:
            break
        elif chunk_size_to_try == min_chunk_size:
            # case where using a chunk size of 1.0 doesn't work
            raise Exception(
                f"Unable to create concept model for '{concept_term}'. Please try using a different concept term."
            )

    return full_pred_arr


# Returns a continous (0-1 score) prediction for the provided concept term on the provided example x. The example must be an image path (local file or remote URL).
def get_img_concept_pred(x, concept_term, input_type, debug):
    # Load image
    if input_type == InputType.ImageLocal:
        # x is local file path
        img = Image.open(x)
    elif input_type == InputType.Image:
        # x is remote image URL
        response = requests.get(x)
        img = Image.open(BytesIO(response.content))
        img = rescale_img(img)

    # Get prediction
    pred = image_text_similarity(CLIP_MODEL, CLIP_PREPROCESS, img, concept_term).item()

    return pred


# Returns a continous (0-1 score) prediction for the provided concept term on the provided example x. The example must be an image path (local file or remote URL).
def get_img_concept_pred_batch(x_arr, concept_term, input_type, debug):
    pred_arr = []
    for x in x_arr:
        # Load image
        if input_type == InputType.ImageLocal:
            # x is local file path
            img = Image.open(x)
        elif input_type == InputType.Image:
            # x is remote image URL
            response = requests.get(x)
            img = Image.open(BytesIO(response.content))
            img = rescale_img(img)

        # Get prediction
        pred = image_text_similarity(
            CLIP_MODEL, CLIP_PREPROCESS, img, concept_term
        ).item()
        pred_arr.append(pred)

    return pred_arr
