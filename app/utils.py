# Adapted from
# https://github.com/mansuf/mangadex-downloader/blob/v2.10.3/mangadex_downloader/utils.py#L105-L119
# with some modifications
def comma_separated_text(array):
    # Opening square bracket
    text = "["

    if not array:
        text += "]"
        return text

    # Append first item
    text += array.pop(0)

    # Add the rest of items
    for item in array:
        text += ", " + item

    # Closing square bracket
    text += "]"

    return text
