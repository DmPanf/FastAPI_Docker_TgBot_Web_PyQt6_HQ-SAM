# menu_styles.py

from PyQt6.QtWidgets import QPushButton, QRadioButton

# Стили для оформления виджетов и кнопок
borderStyle = """
border: 2px solid darkviolet;
border-radius: 5px;
margin: 1px;
border: 2px solid white;
"""

btnStyle = f"""
QPushButton {{
    background-color: darkgreen;
    padding: 10px;
    color: white;
    font-size: 16px;
    {borderStyle}
}}
QPushButton:hover {{
    background-color: limegreen;
}}
"""

menubtnStyle = f"""
QPushButton {{
    background-color: darkgreen;
    padding: 5px;
    color: white;
    font-size: 16px
}}
QPushButton:hover {{
    background-color: limegreen;
}}
"""

radiobtnStyle = f"""
QRadioButton {{
    font-size: 16px
    padding: 50px
    color: lightgreen
    background-color: darkgray
}}
"""
