import yaml
import numpy as np
from markdownify import markdownify as md
import re

from src.model.searching_info import SearchingInfo



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
    searching_info: SearchingInfo,
    threshold: float
) -> SearchingInfo:
    
    contexts = np.array(searching_info.contexts)
    scores = np.array(searching_info.scores)
    indices = np.array(searching_info.indices)

    confident_index = np.where(scores > threshold)[0]

    if confident_index.shape[0] == 0:

        return SearchingInfo(
            scores=[],
            contexts=[],
            indices=[]
        )
    
    confident_indices = indices[confident_index].tolist()
    confident_contexts = contexts[confident_index].tolist()
    confident_scores = scores[confident_index].tolist()
    
    return SearchingInfo(
        scores=confident_scores,
        contexts=confident_contexts,
        indices=confident_indices
    )
    


def convert_html2markdown(html_content: str) -> str:
    markdown_content = md(html_content)
    markdown_content = re.sub("\n\n+", "\n", markdown_content)
    return markdown_content