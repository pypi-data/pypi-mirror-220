""" Prompt to generate Python code for multiple dataframes """

from datetime import date

import pandas as pd

from .base import Prompt


class MultipleDataframesPrompt(Prompt):
    """Prompt to generate Python code"""

    text: str = """
Today is {today_date}.
You are provided with the following pandas dataframes:"""
    instruction: str = """
When asked about the data, your response should include a python code that describes the dataframes provided.
Don't add too many code comments.The result must be printed at the end of the python code.If the data format is not standard, standardize and format the data first.
Using the provided dataframes and no other dataframes, return the python code to get the answer to the following question:
"""  # noqa: E501

    def __init__(self, dataframes: list[pd.DataFrame]):
        for i, dataframe in enumerate(dataframes, start=1):
            row, col = dataframe.shape

            dfhead = dataframe.head(5).to_csv(index=False)

            self.text += f"""
Dataframe df{i}, with {row} rows and {col} columns.
This is the first 5 rows of the dataframe df{i}:
{dfhead}"""


        self.text += self.instruction
        self.text = self.text.format(
            today_date=date.today(),
        )

    def __str__(self):
        return self.text
