from PIL import Image, ImageDraw, ImageFont, ImageOps
import csv
from pprint import pprint

CARD_SIZE = CARD_WIDTH, CARD_HEIGHT = 530, 800

BLANK_FRONT = Image.open("front.png")
BLANK_BACK = Image.open("back.png")

TITLE_DEED_FONT = ImageFont.FreeTypeFont("inter-bold.ttf", 20)
TITLE_FONT = ImageFont.FreeTypeFont("lora.ttf", 48)
DOLLAR_VALUES_FONT = ImageFont.FreeTypeFont("inter-medium.ttf", 36)
MORTGAGE_FONT = TITLE_FONT  # stroke of luck here
UNMORTGAGE_FONT = ImageFont.FreeTypeFont("lora.ttf", 96)

GROUP_COLOURS = {
    "A": ("#783F04", "#FFFFFF"),
    "B": ("#CFE2F3", "#000000"),
    "C": ("#A64D79", "#FFFFFF"),
    "D": ("#FF9900", "#000000"),
    "E": ("#CC0000", "#FFFFFF"),
    "F": ("#F1C232", "#000000"),
    "G": ("#38761D", "#FFFFFF"),
    "H": ("#0B5394", "#FFFFFF"),
}


class PropertyCard:
    def __init__(
        self,
        index,
        group,
        title,
        rent,
        with_colour_set,
        with_one_house,
        with_two_houses,
        with_three_houses,
        with_four_houses,
        with_hotel,
        house_cost,
        hotel_cost,
        mortgage,
        mortgage_payment,
    ) -> None:
        self.index = index
        self.group = group
        self.title = title
        self.rent = rent
        self.with_colour_set = with_colour_set
        self.with_one_house = with_one_house
        self.with_two_houses = with_two_houses
        self.with_three_houses = with_three_houses
        self.with_four_houses = with_four_houses
        self.with_hotel = with_hotel
        self.house_cost = house_cost
        self.hotel_cost = hotel_cost
        self.mortgage = mortgage
        self.mortgage_payment = mortgage_payment

    def __repr__(self) -> str:
        return f"PropertyCard(index={self.index}, group={self.group}, title={self.title}, rent={self.rent}, with_colour_set={self.with_colour_set}, with_one_house={self.with_one_house}, with_two_houses={self.with_two_houses}, with_three_houses={self.with_three_houses}, with_four_houses={self.with_four_houses}, with_hotel={self.with_hotel}, house_cost={self.house_cost}, hotel_cost={self.hotel_cost}, mortgage={self.mortgage}, mortgage_payment={self.mortgage_payment})"


def read_properties() -> list[PropertyCard]:
    with open("properties.csv") as file:
        properties = []
        for row in csv.reader(file):
            (
                row_group,
                name,
                rent,
                with_set,
                with_one_house,
                with_two_houses,
                with_three_houses,
                with_four_houses,
                with_hotel,
                house_cost,
                hotel_cost,
                mortgage,
                unmortgage,
            ) = row
            if row_group.strip() != "":
                group = row_group
                group_index = 1
            else:
                group_index += 1

            properties.append(
                PropertyCard(
                    f"{group}{group_index}",
                    group,
                    name,
                    rent,
                    with_set,
                    with_one_house,
                    with_two_houses,
                    with_three_houses,
                    with_four_houses,
                    with_hotel,
                    house_cost,
                    hotel_cost,
                    mortgage,
                    unmortgage,
                )
            )

    return properties


def generate_card(property: PropertyCard):
    generate_card_front(property)
    generate_card_back(property)


def generate_card_heading(
    property: PropertyCard,
    canvas: Image.Image,
    draw: ImageDraw,
    bw: bool = False,
):
    head_background, head_foreground = GROUP_COLOURS[property.group]

    with Image.open(f"images/{property.index}.png") as head_image:
        head_image = head_image.resize((494, 154))
        head_image = head_image.convert("RGBA")
        if bw:
            head_image = ImageOps.grayscale(head_image)
        canvas.paste(head_image, (18, 18, 18 + 494, 18 + 154))

    draw.rounded_rectangle((40, 108, 44 + 443 + 4, 112 + 112 + 4), 30, "#FFFFFF")
    draw.rounded_rectangle((44, 112, 44 + 443, 112 + 112), 26, head_background)
    draw.text(
        (266, 130),
        "MORTGAGED PROPERTY" if bw else "TITLE DEED",
        head_foreground,
        TITLE_DEED_FONT,
        anchor="mt",
    )
    draw.text((266, 180), property.title, head_foreground, TITLE_FONT, anchor="mm")


def generate_card_front(property: PropertyCard):
    with Image.new("RGB", CARD_SIZE, "#000000") as canvas:
        draw = ImageDraw.Draw(canvas)
        canvas.paste(BLANK_FRONT)
        generate_card_heading(property, canvas, draw)

        draw.text(
            (487, 286),
            property.rent,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (487, 286 + 52),
            property.with_colour_set,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (487, 286 + 2 * 52),
            property.with_one_house,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (487, 286 + 3 * 52),
            property.with_two_houses,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (487, 286 + 4 * 52),
            property.with_three_houses,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (487, 286 + 5 * 52),
            property.with_four_houses,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (487, 286 + 6 * 52),
            property.with_hotel,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )

        draw.text(
            (394, 680),
            property.house_cost,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )
        draw.text(
            (394, 680 + 52),
            property.hotel_cost,
            "#000000",
            DOLLAR_VALUES_FONT,
            anchor="rs",
            features=["tnum"],
        )

        canvas.save(f"output/{property.index}-A.png")


def generate_card_back(property: PropertyCard):
    with Image.new("RGB", CARD_SIZE, "#FFFFFF") as canvas:
        draw = ImageDraw.Draw(canvas)
        canvas.paste(BLANK_BACK)
        generate_card_heading(property, canvas, draw, bw=True)

        draw.text(
            (265, 347),
            property.mortgage,
            "#FFFFFF",
            MORTGAGE_FONT,
            anchor="mm",
        )
        draw.text(
            (265, 511),
            property.mortgage_payment,
            "#FFFFFF",
            UNMORTGAGE_FONT,
            anchor="mm",
        )

        canvas.save(f"output/{property.index}-B.png")


if __name__ == "__main__":
    properties = read_properties()
    for property in properties:
        print(property.index)
        generate_card(property)
