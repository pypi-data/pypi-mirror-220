# text-selection-component

Streamlit component to get slected text in paragraph so, you process selected text

## Installation instructions 

```sh
pip install text-selection-component
```

## Usage instructions

```python
import streamlit as st

from text_selection_component import text_selection_component

value = text_selection_component()

st.write(value)
