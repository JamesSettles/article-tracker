import matplotlib.pyplot as plt
import os
import io
from datetime import datetime

def generate_stats(memory_filename='article_memory.txt')->dict:
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
            data = {
                'date': None,
                'page_count': 0,
                'word_count': 0,
                'articles': 0
            }
            for line in lines:
                if line.startswith("Date Submitted:"):
                    if data['date']:
                        month = data['date'].strftime('%Y-%m')
                        if month not in stats['months']:
                            stats['months'].append(month)
                            stats['article_counts'].append(data['articles'])
                            stats['page_counts'].append(data['page_count'])
                            stats['word_counts'].append(data['word_count'])
                        else:
                            index = stats['months'].index(month)
                            stats['article_counts'][index] += data['articles']
                            stats['page_counts'][index] += data['page_count']
                            stats['word_counts'][index] += data['word_count']
                    
                    data = {
                        'date': datetime.strptime(line.split(': ')[1].strip(), '%Y-%m-%d'),
                        'page_count': 0,
                        'word_count': 0,
                        'articles': 0
                    }
                elif line.startswith("Page Count:"):
                    data['page_count'] += int(line.split(': ')[1].strip())
                elif line.startswith("Word Count:"):
                    data['word_count'] += int(line.split(': ')[1].strip())
                elif line.startswith("Title:"):
                    data['articles'] += 1

            # Append last read data
            if data['date']:
                month = data['date'].strftime('%Y-%m')
                if month not in stats['months']:
                    stats['months'].append(month)
                    stats['article_counts'].append(data['articles'])
                    stats['page_counts'].append(data['page_count'])
                    stats['word_counts'].append(data['word_count'])
                else:
                    index = stats['months'].index(month)
                    stats['article_counts'][index] += data['articles']
                    stats['page_counts'][index] += data['page_count']
                    stats['word_counts'][index] += data['word_count']
    return stats

def create_stats_graph(stats:dict):
    """
    Uses matplotlib to return a bar graph image based off of the stats. 
    """
    # Create bar graph
    fig, ax = plt.subplots()
    width = 0.2
    x = range(len(stats['months']))

    ax.bar([i - width for i in x], stats['article_counts'], width, label='Articles')
    ax.bar(x, stats['page_counts'], width, label='Pages')
    ax.bar([i + width for i in x], stats['word_counts'], width, label='Words')

    ax.set_xlabel('Month')
    ax.set_ylabel('Count')
    ax.set_title('Monthly Statistics')
    ax.set_xticks(x)
    ax.set_xticklabels(stats['months'])
    ax.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return img