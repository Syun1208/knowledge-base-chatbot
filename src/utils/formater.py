import re


def format_text(text):
    # Step 1: Remove excess whitespace and ensure consistent formatting
    text = re.sub(r'\n+', '\n', text.strip())
    
    # Step 2: Break the text into major sections based on patterns like '------'
    sections = re.split(r'\n[-=]+\n', text)
    
    formatted_text = ''
    
    for section in sections:
        # Step 3: For each section, process the title and content
        lines = section.strip().split('\n')
        title = lines[0]
        content = '\n'.join(lines[1:])
        
        # Step 4: Add title to formatted text
        formatted_text += title + '\n' + '-' * len(title) + '\n'
        
        # Step 5: Handle indentation for nested bullet points
        formatted_text += format_content(content) + '\n\n'
    
    return formatted_text.strip()



def format_content(content):
    lines = content.split('\n')
    formatted_lines = []
    indent_level = 0

    for line in lines:
        if line.startswith('-'):
            # Bullet points, so we add indentation
            formatted_lines.append('  ' * indent_level + line)
        else:
            # Non-bullet point, reset indentation
            if line.strip() == '':
                formatted_lines.append('')
            else:
                formatted_lines.append('  ' * indent_level + line)
        
        # Increase indent if the line is a section heading
        if re.search(r'[A-Za-z\s]+$', line):
            indent_level += 1
    
    return '\n'.join(formatted_lines)



def format_content_for_markdown(content):
    lines = content.split('\n')
    formatted_lines = []
    indent_level = 0

    for line in lines:
        if line.startswith('-'):
            # Bullet points, add indentation
            formatted_lines.append('  ' * indent_level + line)
        else:
            # Non-bullet point, reset indentation
            if line.strip() == '':
                formatted_lines.append('')
            else:
                formatted_lines.append('  ' * indent_level + line)
        
        # Increase indent if the line is a sub-section heading
        if re.search(r'[A-Za-z\s]+$', line):
            indent_level += 1
    
    return '\n'.join(formatted_lines)



def format_to_markdown(text):
    # Step 1: Remove excess whitespace and ensure consistent formatting
    text = re.sub(r'\n+', '\n', text.strip())
    
    # Step 2: Break the text into major sections based on patterns like '------'
    sections = re.split(r'\n[-=]+\n', text)
    
    markdown_text = ''
    
    for section in sections:
        # Step 3: For each section, process the title and content
        lines = section.strip().split('\n')
        title = lines[0]
        content = '\n'.join(lines[1:])
        
        # Step 4: Add title to markdown text as H1
        markdown_text += f'# {title}\n\n'
        
        # Step 5: Handle indentation for nested bullet points
        markdown_text += format_content_for_markdown(content) + '\n\n'
    
    return markdown_text.strip()