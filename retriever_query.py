import json
import random

# Load the knowledge base (JSON)
def load_kb(file_path):
    with open(file_path, 'r') as f:
        kb = json.load(f)
    return kb

# Function to filter restaurants based on criteria
def query_restaurant_kb(kb, name="", area="", food="", pricerange=""):
        results = []
        for restaurant in kb:
            if (name.lower() in restaurant["name"].lower() or not name) and \
               (area.lower() in restaurant["area"].lower() or not area) and \
               (food.lower() in restaurant["food"].lower() or not food) and \
               (pricerange.lower() in restaurant["pricerange"].lower() or not pricerange):
                results.append(restaurant)
        return results

# Function to return up to N random restaurants from the filtered list
def get_random_restaurants(restaurants, N):
    if len(restaurants) > N:
        return random.sample(restaurants, N)
    else:
        return restaurants

# Main function
def find_restaurants(kb_file, name=None, area=None, pricerange=None, food=None, N=5):
    if not name and not area and not pricerange and not food:
        return
    # Load KB
    kb = load_kb(kb_file)
    
    # Filter restaurants based on criteria
    filtered_restaurants = query_restaurant_kb(kb, name, area, pricerange, food)
    
    # Return up to N random restaurants
    selected_restaurants = get_random_restaurants(filtered_restaurants, N)
    
    return selected_restaurants

if __name__ == "__main__":
    # Example Usage
    kb_file = 'KB/restaurant_db.json'  # Path to your KB JSON file

    # Example search criteria (you can adjust these)
    name = None  # Optional name
    area = None  # Optional area
    pricerange = None  # Optional price range
    food = None  # Optional food type
    N = 5  # Maximum number of restaurants to return

    # Find restaurants based on the criteria
    matching_restaurants = find_restaurants(kb_file, name, area, pricerange, food, N)

    # Display results
    if matching_restaurants:
        for restaurant in matching_restaurants:
            print(restaurant)
