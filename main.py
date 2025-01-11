# TODO #1: Import necessary libraries

import os
import pandas as pd
import taipy.gui.builder as tgb
from dotenv import load_dotenv
from web3 import Web3
from taipy.gui import Gui, notify

# TODO #2: Load environment variables

load_dotenv()

# TODO #3: Define questions for the quiz

questions = [
    {"question": "What is AI?", "answer": "Artificial Intelligence"},
    {"question": "What is Blockchain?", "answer": "A decentralized ledger"},
    {"question": "What does NFT stand for?", "answer": "Non-Fungible Token"},
    # Add more questions as needed
]

# Initialize quiz state variables
current_question_index = 0
user_wallet = None
user_tokens = 0


# TODO #4: Define functions for wallet connection and gameplay logic

def connect_wallet(state):
    global user_wallet
    infura_url = os.getenv("INFURA_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
    web3 = Web3(Web3.HTTPProvider(infura_url))
    if web3.isConnected():
        user_wallet = web3.eth.account.create()
        state.wallet_address = user_wallet.address
        notify(state, "success", f"Wallet connected: {user_wallet.address}")
    else:
        notify(state, "error", "Failed to connect to wallet.")


def check_answer(state):
    global current_question_index, user_tokens
    correct_answer = questions[current_question_index]["answer"].lower()
    if state.query_message.strip().lower() == correct_answer:
        state.messages.append(
            {"style": "assistant_message", "content": "Correct! You earned 10 tokens!"}
        )
        user_tokens += 10
    else:
        state.messages.append(
            {"style": "assistant_message", "content": "Incorrect. Try again!"}
        )
    
    current_question_index = (current_question_index + 1) % len(questions)
    next_question = questions[current_question_index]["question"]
    state.messages.append(
        {"style": "assistant_message", "content": f"Next question: {next_question}"}
    )
    state.query_message = ""
    state.conv.update_content(state, create_conv(state))


def create_conv(state):
    messages_dict = {}
    with tgb.Page() as conversation:
        for i, message in enumerate(state.messages):
            text = message["content"].replace("<br>", "\n").replace('"', "'")
            messages_dict[f"message_{i}"] = text
            tgb.text(
                f"{{messages_dict.get('message_{i}') or ''}}",
                class_name=f"message_base {message['style']}",
                mode="md",
            )
    state.messages_dict = messages_dict
    return conversation


def reset_game(state):
    global current_question_index, user_tokens
    current_question_index = 0
    user_tokens = 0
    state.messages = [
        {"style": "assistant_message", "content": "Welcome to the Quiz Game!"},
        {"style": "assistant_message", "content": questions[current_question_index]["question"]},
    ]
    state.query_message = ""
    state.conv.update_content(state, create_conv(state))


# TODO #5: Design the GUI layout

with tgb.Page() as page:
    with tgb.layout(columns="350px 1"):
        with tgb.part(class_name="sidebar"):
            tgb.text("## Quiz Game: AI & Blockchain", mode="md")
            tgb.button(
                "New Game",
                class_name="fullwidth plain",
                on_action=reset_game,
            )
            tgb.button(
                "Connect Wallet",
                class_name="fullwidth plain",
                on_action=connect_wallet,
            )
            tgb.text("## Wallet Address: <|wallet_address|>", mode="md")
            tgb.text("## Tokens Earned: <|user_tokens|>", mode="md")

        with tgb.part(class_name="p1"):
            tgb.part(partial="{conv}", height="600px", class_name="card card_chat")
            with tgb.part("card mt1"):
                tgb.input(
                    "{query_message}",
                    on_action=check_answer,
                    change_delay=-1,
                    label="Write your answer:",
                    class_name="fullwidth",
                )


# TODO #6: Add the application run logic

if __name__ == "__main__":
    gui = Gui(page)
    conv = gui.add_partial("")
    gui.run(
        title="Quiz Game: AI & Blockchain",
        dark_mode=False,
        margin="0px",
        debug=True,
    )
