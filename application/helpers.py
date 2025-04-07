import os
import json
from openai import OpenAI
from config import TEXT_PATH
from openai.types.chat import ChatCompletionMessageParam


def is_active(current_path:str, nav_path:str) -> str:
    """Returns a string that shows which page is active in the navigation menu."""

    if current_path == nav_path:
        return "is-active"
    
    return ""


def read_description(file_path:str) -> list:
    """Returns the content of a text file as a list of strings where each string is a paragraph."""

    content = []

    try:
        with open(file_path) as file:
            current_paragraph = ""

            # Loop over each line
            for line in file:
                # Check if the line is blank (i.e. contains only white spaces)
                if line.strip() == "":
                    # If so, add the current paragraph to the list and reset current paragraph
                    content.append(current_paragraph)
                    current_paragraph = ""
                # If line is not blank, add it to the current paragraph
                else:
                    current_paragraph += line

            # Add the final paragraph to the list
            if current_paragraph != "":
                content.append(current_paragraph)
    except FileNotFoundError:
        print(f"ERROR! File could not be found for path: {file_path}.")
    except Exception as error:
        print(f"ERROR! {error}.")

    return content


def get_skills(file_path:str) -> tuple:
    """Returns three lists one for each type of cards in the JSON file."""

    try:
        with open(file_path) as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"ERROR! File could not be found for path: {file_path}.")
    except json.JSONDecodeError as error:
        print(f"ERROR! {error}.")
    except Exception as error:
        print(f"ERROR! {error}.")

    # Storing the information based on the type of card
    software = [card for card in data["cards"] if card["type"] == "software"]
  
    return software

def get_language_image(language:str) -> str:
    """Returns the image of a programming language from 'skills.json'."""

    try:
        with open(f"{TEXT_PATH}/skills.json") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        print(f"ERROR! {error}.")
    else:
        for card in data.get("cards", []):
            if card.get("type") == "language" and card.get("title", "").lower() == language.lower():
                return card.get("image")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text(prompt: str) -> str:
    try:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": (
                    "你是一名很專業的影像創作者,在剪輯以及拍攝都是以旅行居多，然後熟悉鏡位調整與剪輯節奏以幽默風趣的回答"
                    "請用繁體中文回答使用者的問題。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18"),
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "系統錯誤，請稍後再試～"