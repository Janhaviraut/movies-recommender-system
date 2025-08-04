import pandas as pd
import pickle

# Step 1: Read your CSV file
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')# Change filename if needed

# Step 2: Save the data as movies.pkl
with open('movies.pkl', 'wb') as f:
    pickle.dump(movies, f)

print("✅ movies.pkl created from your CSV!")