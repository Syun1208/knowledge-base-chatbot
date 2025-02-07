import yaml
import numpy as np
from markdownify import markdownify as md
from bs4 import BeautifulSoup

from langdetect import detect
from deep_translator import GoogleTranslator
import re
from src.model.searching_information import SearchingInformation



def load_yaml(file_path: str):
    """
    Load a YAML file.
    
    Args:
        file_path (str): Path to the YAML file.
    
    Returns:
        dict: Parsed YAML data as a dictionary.
    """
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None
    
    
    
def get_confident_context(
    searching_info: SearchingInformation,
    threshold: float
) -> SearchingInformation:
    
    contexts = np.array(searching_info.contexts)
    urls = np.array(searching_info.urls)
    scores = np.array(searching_info.scores)
    indices = np.array(searching_info.indices)

    confident_index = np.where(scores > threshold)[0]

    if confident_index.shape[0] == 0:

        return SearchingInformation(
            scores=[],
            contexts=[],
            urls=[],
            indices=[]
        )
    
    confident_indices = indices[confident_index].tolist()
    confident_contexts = contexts[confident_index].tolist()
    confident_urls = urls[confident_index].tolist()
    confident_scores = scores[confident_index].tolist()
    
    return SearchingInformation(
        scores=confident_scores,
        contexts=confident_contexts,
        urls=confident_urls,
        indices=confident_indices
    )
    


def convert_html2markdown(html_content: str) -> str:
    markdown_content = md(html_content)
    markdown_content = re.sub("\n\n+", "\n", markdown_content)
    return markdown_content

def split_html_into_section_dict(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    sections = []
    current_h1 = "Untitled Section"  # Ensure a default H1 section
    current_h2 = None
    current_h3 = None

    structure = {current_h1: {}}  # Start with a default section

    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'table']):
        tag_md = md(str(tag)).strip()
        
        if tag.name == 'h1':  # New Major Section
            current_h1 = tag_md
            current_h2 = None
            current_h3 = None
            structure[current_h1] = {}

        elif tag.name == 'h2':  # New Subsection under H1
            if current_h1 not in structure:
                structure[current_h1] = {}
            current_h2 = tag_md
            current_h3 = None
            structure[current_h1][current_h2] = []

        elif tag.name == 'h3':  # New Sub-subsection under H2
            if current_h2 is None:
                current_h2 = "Untitled Subsection"
                structure[current_h1][current_h2] = []
            current_h3 = tag_md
            structure[current_h1][current_h2].append({current_h3: []})

        else:  # Content (belongs to nearest header)
            content = tag_md + "\n\n"
            if current_h3:  # Under H3
                structure[current_h1][current_h2][-1][current_h3].append(content)
            elif current_h2:  # Under H2
                structure[current_h1][current_h2].append(content)
            else:  # Under H1 directly
                if "_content" not in structure[current_h1]:
                    structure[current_h1]["_content"] = []
                structure[current_h1]["_content"].append(content)

    return structure

# Convert structured data to Markdown
def format_markdown(structure, level=1):
    md_output = ""
    for key, value in structure.items():
        if key == "_content":  # Handle raw content at the top level
            for content in value:
                md_output += content
            continue
        md_output += f"{'#' * level} {key}\n\n"
        if isinstance(value, list):  # H2 or H3 content
            for item in value:
                if isinstance(item, dict):  # H3 subsection
                    md_output += format_markdown(item, level + 1)
                else:  # Regular content
                    md_output += item
        else:  # H2 and beyond
            md_output += format_markdown(value, level + 1)
    return md_output


def detect_and_translate(text):
    try:
        lang = detect(text)
        if lang == "en":
            return text
        return GoogleTranslator(source=lang, target="en").translate(text)
    except Exception as e:
        print(f"Error: {e}")
        return text