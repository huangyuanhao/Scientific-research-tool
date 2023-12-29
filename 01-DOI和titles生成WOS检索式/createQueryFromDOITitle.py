import pandas as pd

# Load the CSV file
file_path = '文献信息.csv'
df = pd.read_csv(file_path)

# Function to generate Web of Science search query
def generate_search_query(row):
    if pd.notnull(row['DOI']):
        return f'DO=("{row["DOI"]}")'
    else:
        return f'TI=("{row["Title"]}")'

# Apply the function to each row and join queries with ' OR '
search_queries = df.apply(generate_search_query, axis=1)
final_query = ' OR '.join(search_queries)

print(final_query)


with open('search_query.txt', 'w', encoding='utf-8') as f:
    f.write(final_query)
