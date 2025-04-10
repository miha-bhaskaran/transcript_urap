import boto3
import csv
import os
from PIL import Image, ImageDraw  # Importing Pillow for image manipulation


def extract_text_from_image(image_path):

    textract = boto3.client("textract")

    # Load the image
    with open(image_path, "rb") as document:
        image_bytes = document.read()

    # Call Textract to analyze the document
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES", "FORMS"]
    )

    return response


def extract_tables_from_response(response):
    blocks = response["Blocks"]
    tables = [block for block in blocks if block["BlockType"] == "TABLE"]

    extracted_tables = []

    for table in tables:
        rows = {}
        for relationship in table["Relationships"]:
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    cell = next(block for block in blocks if block["Id"] == child_id)
                    if cell["BlockType"] == "CELL":
                        row_index = cell["RowIndex"]
                        col_index = cell["ColumnIndex"]
                        if row_index not in rows:
                            rows[row_index] = {}
                        rows[row_index][col_index] = cell

        table_data = []
        max_col_index = max(max(row.keys()) for row in rows.values())
        for row_index in sorted(rows.keys()):
            row_data = []
            for col_index in range(1, max_col_index + 1):
                if col_index in rows[row_index]:
                    text = ""
                    for relationship in rows[row_index][col_index].get(
                        "Relationships", []
                    ):
                        if relationship["Type"] == "CHILD":
                            for child_id in relationship["Ids"]:
                                word = next(
                                    block for block in blocks if block["Id"] == child_id
                                )
                                if word["BlockType"] == "WORD":
                                    text += word["Text"] + " "
                    text = text.strip()

                else:
                    text = ""
                row_data.append(text)
            table_data.append(row_data)

        extracted_tables.append(table_data)

    return extracted_tables


def draw_bounding_boxes_on_image(image, blocks):
    draw = ImageDraw.Draw(image, "RGBA")  # 'RGBA' mode to allow transparency
    width, height = image.size

    for block in blocks:
        print(block)
        if block["BlockType"] == "CELL" and "Geometry" in block:
            bounding_box = block["Geometry"]["BoundingBox"]
            left = bounding_box["Left"] * width
            top = bounding_box["Top"] * height
            box_width = bounding_box["Width"] * width
            box_height = bounding_box["Height"] * height

            # Get the confidence level
            confidence = block.get("Confidence", 100)  # Default to 100 if not present

            # Map confidence to color intensity (0-255), lower confidence means more transparency
            intensity = int(255 * (confidence / 100))  # Map confidence to a 0-255 range

            # Set the shading color (RGBA) based on confidence
            shading_color = (
                255,
                0,
                0,
                intensity,
            )  # Red color with variable transparency

            # Draw shaded rectangle
            draw.rectangle(
                [left, top, left + box_width, top + box_height], fill=shading_color
            )

            # Optionally, draw the outline of the box with a solid color
            draw.rectangle(
                [left, top, left + box_width, top + box_height],
                outline="black",
                width=2,
            )

    return image


# def save_tables_to_csv(tables, csv_filename):
#     with open(csv_filename, 'w', newline='') as csvfile:
#         csvwriter = csv.writer(csvfile)
#         for table in tables:
#             for row in table:
#                 csvwriter.writerow(row)
#             csvwriter.writerow([])
def save_table_to_csv(table, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in table:
            csvwriter.writerow(row)


def process_images_in_folder(folder_path):
    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            response = extract_text_from_image(image_path)

            # Load the image using PIL
            image = Image.open(image_path)

            # Draw bounding boxes on the image
            image_with_boxes = draw_bounding_boxes_on_image(image, response["Blocks"])

            # Save the image with bounding boxes
            image_with_boxes.save(
                os.path.join(
                    folder_path, f"{os.path.splitext(filename)[0]}_bounding.png"
                ),
                "PNG",
            )

            tables = extract_tables_from_response(response)

            # Save each table to its own CSV file
            for i, table in enumerate(tables):
                csv_filename = os.path.join(
                    folder_path, f"{os.path.splitext(filename)[0]}_table_{i + 1}.csv"
                )
                save_table_to_csv(table, csv_filename)
                print(
                    f"Extracted table {i + 1} from {filename} has been saved to {csv_filename}"
                )
