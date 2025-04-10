import base64


def encode_image_to_base64(image_path, output_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    with open(output_path, "w") as output_file:
        output_file.write(base64_image)


encode_image_to_base64("input_example.png", "input_example.txt")
