import os
import webbrowser
import time

# पहले ब्राउज़र खोलें
webbrowser.open("http://localhost:8501")

# फिर स्ट्रीमलिट चलाएं
os.system("streamlit run webapp.py")