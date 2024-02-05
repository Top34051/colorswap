import json
from datasets import load_dataset


def extract_options_text(text):
    text = text.removeprefix("Does this image present (A) ")
    text = text.removesuffix("? Note, you must choose one of the two options")
    text = text.removesuffix(
        "? First, describe the image information relevant to the question. Then, provide your answer. Note you must choose one of the two options"
    )
    options = text.split(", or (B) ")
    return options


def is_option_text(response, option_text, alternative_text, option="A", alternative="B"):
    if option_text.lower() in response.lower() and alternative_text.lower() not in response.lower():
        return True
    if f"image presents ({option})".lower() in response.lower():
        return True
    if f"image presents option ({option})".lower() in response.lower():
        return True
    if f"image presents option {option}".lower() in response.lower():
        return True
    if response.startswith(f"{option})") or response.startswith(f"({option})"):
        return True
    if (
        response.startswith(f"Option {option}")
        or response.startswith(f"Option {option})")
        or response.startswith(f"Option ({option})")
    ):
        return True
    if (
        f"option {option}".lower() in response.lower()
        or f"option ({option})".lower() in response.lower()
        or f"option {option})".lower() in response.lower()
    ) and not (f"({alternative})".lower() in response.lower() or f"{alternative})".lower() in response.lower()):
        return True
    if response == option:
        return True
    if f"it would imply ({option})".lower() in response.lower():
        return True
    if f"it could metaphorically represent ({option})".lower() in response.lower():
        return True
    if f"it is ({option})".lower() in response.lower():
        return True
    if f"this image presents {option_text}".lower() in response.lower():
        return True

    def remove_p(text):
        text = (
            text.replace(" a ", " ")
            .replace(" an ", " ")
            .replace(" the ", " ")
            .replace(" with ", " ")
            .replace(" and ", " ")
        )
        text = text.removeprefix("a ")
        text = text.removeprefix("an ")
        text = text.removeprefix("the ")
        return text

    if (
        remove_p(option_text).lower() in remove_p(response).lower()
        and remove_p(alternative_text).lower() not in remove_p(response).lower()
    ):
        return True
    return False


def is_option_image(response, option_text, alternative_text, option="first", alternative="second"):
    if option in response.lower() and alternative not in response.lower():
        return True
    if f"{option} image better aligns" in response.lower() or f"{option} image aligns better" in response.lower():
        return True
    if f"the {option} image is more relevant" in response.lower():
        return True
    return False


if __name__ == "__main__":
    show_warning = False
    for model in ["gpt4v", "llava", "llavar"]:
        for dataset in ["colorswap"]:
            # text score
            response = json.load(open(f"results/text-{model}-{dataset}.json"))
            text_scores = []
            for sample in response:
                if "error" in sample:
                    continue

                options = extract_options_text(sample["prompt_image_1"])
                option_a = is_option_text(sample["response_image_1"], options[0], options[1], "A", "B")
                option_b = is_option_text(sample["response_image_1"], options[1], options[0], "B", "A")
                chosen_image_1 = {
                    (0, 0): None,
                    (0, 1): "B",
                    (1, 0): "A",
                    (1, 1): None,
                }[(option_a, option_b)]

                options = extract_options_text(sample["prompt_image_2"])
                option_a = is_option_text(sample["response_image_2"], options[0], options[1], "A", "B")
                option_b = is_option_text(sample["response_image_2"], options[1], options[0], "B", "A")
                chosen_image_2 = {
                    (0, 0): None,
                    (0, 1): "B",
                    (1, 0): "A",
                    (1, 1): None,
                }[(option_a, option_b)]

                if show_warning and (chosen_image_1 is None or chosen_image_2 is None):
                    print("warning: no answer found for sample", sample["id"], chosen_image_1, chosen_image_2)
                    print("  options:", options)
                    print("  response_image_1:", sample["response_image_1"])
                    print("  response_image_2:", sample["response_image_2"])
                    print()

                text_scores.append(
                    sample["log_1"]["correct_answer"] == chosen_image_1
                    and sample["log_2"]["correct_answer"] == chosen_image_2
                )

            # image score
            image_scores = []
            response = json.load(open(f"results/image-{model}-{dataset}.json"))
            for sample in response:
                if "error" in sample:
                    continue

                option_first = is_option_image(sample["response_caption_1"], options[0], options[1], "first", "second")
                option_second = is_option_image(sample["response_caption_1"], options[1], options[0], "second", "first")
                chosen_caption_1 = {
                    (0, 0): None,
                    (0, 1): "second",
                    (1, 0): "first",
                    (1, 1): None,
                }[(option_first, option_second)]

                option_first = is_option_image(sample["response_caption_2"], options[0], options[1], "first", "second")
                option_second = is_option_image(sample["response_caption_2"], options[1], options[0], "second", "first")
                chosen_caption_2 = {
                    (0, 0): None,
                    (0, 1): "second",
                    (1, 0): "first",
                    (1, 1): None,
                }[(option_first, option_second)]

                if show_warning and (chosen_caption_1 is None or chosen_caption_2 is None):
                    print("warning: no answer found for sample", sample["id"], chosen_caption_1, chosen_caption_2)
                    print("  response_caption_1:", sample["response_caption_1"])
                    print("  response_caption_2:", sample["response_caption_2"])
                    print()

                image_scores.append(
                    chosen_caption_1 == sample["log_1"]["correct_answer"]
                    and chosen_caption_2 == sample["log_2"]["correct_answer"]
                )

            group_scores = [text_score and image_score for text_score, image_score in zip(text_scores, image_scores)]

            print("Model:", model)
            print()
            print("Dataset:", dataset)
            print("Text score:\t{:.2f}".format(sum(text_scores) / len(text_scores) * 100))
            print("Image score:\t{:.2f}".format(sum(image_scores) / len(image_scores) * 100))
            print("Group score:\t{:.2f}".format(sum(group_scores) / len(group_scores) * 100))
            print()
