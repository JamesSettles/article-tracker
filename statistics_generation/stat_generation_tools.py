import matplotlib.pyplot as plt
import os
import io
import sys
from datetime import datetime

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def generate_stats(memory_filename='app/memory/article_memory.txt')->dict:
    """
    Creates article statistics based off of the memory file.
    """
    stats = {
        'months': [],
        'article_counts': [],
        'page_counts': [],
        'word_counts': []
    }
    if os.path.exists(memory_filename):
        with open(memory_filename, 'r') as file:
            lines = file.readlines()
        monthly_data = {}
        current_entry = {}

        for line in lines:
            line = line.strip()
            if not line:
                # Empty line indicates the end of an entry
                date = current_entry.get('Date Submitted')
                if date:
                    month = date.strftime('%Y-%m')
                    if month not in monthly_data:
                        monthly_data[month] = {
                            'articles': 0,
                            'pages': 0,
                            'words': 0
                        }
                    monthly_data[month]['articles'] += 1
                    monthly_data[month]['pages'] += current_entry.get('Page Count', 0)
                    monthly_data[month]['words'] += current_entry.get('Word Count', 0)
                current_entry = {}
            else:
                key, value = line.split(': ', 1)
                if key == 'Date Submitted':
                    value = datetime.strptime(value, '%Y-%m-%d')
                elif key in ['Page Count', 'Word Count']:
                    value = int(value)
                current_entry[key] = value

        # Append any remaining data
        if current_entry:
            date = current_entry.get('Date Submitted')
            if date:
                month = date.strftime('%Y-%m')
                if month not in monthly_data:
                    monthly_data[month] = {
                        'articles': 0,
                        'pages': 0,
                        'words': 0
                    }
                monthly_data[month]['articles'] += 1
                monthly_data[month]['pages'] += current_entry.get('Page Count', 0)
                monthly_data[month]['words'] += current_entry.get('Word Count', 0)

        stats['months'] = list(monthly_data.keys())
        for month in stats['months']:
            stats['article_counts'].append(monthly_data[month]['articles'])
            stats['page_counts'].append(monthly_data[month]['pages'])
            stats['word_counts'].append(monthly_data[month]['words'])

    # Print stats for debugging
    print(f"Months: {stats['months']}")
    print(f"Article Counts: {stats['article_counts']}")
    print(f"Page Counts: {stats['page_counts']}")
    print(f"Word Counts: {stats['word_counts']}")

    # Check if there's any data to plot
    return stats

def create_stats_graph(stats:dict):
    """
    Uses matplotlib to create a bar graphs based off of the stats. 
    """
     # Create bar graphs
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Article Count Graph
    axs[0].bar(stats['months'], stats['article_counts'], color='blue')
    axs[0].set_title('Articles Read per Month')
    axs[0].set_xlabel('Month')
    axs[0].set_ylabel('Number of Articles')

    # Page Count Graph
    axs[1].bar(stats['months'], stats['page_counts'], color='green')
    axs[1].set_title('Pages Read per Month')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Number of Pages')

    # Word Count Graph
    axs[2].bar(stats['months'], stats['word_counts'], color='red')
    axs[2].set_title('Words Read per Month')
    axs[2].set_xlabel('Month')
    axs[2].set_ylabel('Number of Words')

    # Adjust layout and save the plots to a BytesIO object
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)


    return img