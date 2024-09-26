from utils import load_json, write_json
import random
import copy

AUGM_SCALE = 2

original_restaurants = load_json("KB/restaurant_db.json")

all_names = [restaurant['name'].split() for restaurant in original_restaurants]

# Function to generate a random phone number
def generate_random_phone(existing_phones):
    new_phone = str(random.randint(1000000000, 9999999999))
    while new_phone in existing_phones:
        new_phone = str(random.randint(1000000000, 9999999999))
    return new_phone    

# Function to generate a random ID
def generate_random_id(existing_ids):
    new_id = str(random.randint(1000, 9999))
    while new_id in existing_ids:
        new_id = str(random.randint(1000, 9999))
    return new_id

def generate_random_name(existing_names):
    i = 0
    name = ""
    while(1):
        random_name = random.choice(all_names)
        if len(random_name) > i:
            name += random_name[i] + " "
            i += 1
        else:
            name = name[:-1]
            break
    while name in existing_names:
        i = 0
        name = ""
        while(1):
            random_name = random.choice(all_names)
            if len(random_name) > i:
                name += random_name[i] + " "
                i += 1
            else:
                name = name[:-1]
                break
    return name

# Function to generate a random location within a reasonable range
def generate_random_location():
    return [round(random.uniform(52.2000, 52.2200), 5), round(random.uniform(0.1000, 0.1300), 5)]

# Function to create a new restaurant
def create_restaurant(original_restaurants, existing_ids, existing_phones, existing_names):

    # Randomly select food, area, and pricerange from original restaurants
    food = random.choice([restaurant['food'] for restaurant in original_restaurants])
    area = random.choice([restaurant['area'] for restaurant in original_restaurants])
    pricerange = random.choice([restaurant['pricerange'] for restaurant in original_restaurants])

    # Match the address and postcode based on the chosen area
    address_data = [restaurant for restaurant in original_restaurants if restaurant['area'] == area]
    address = random.choice(address_data)['address']
    postcode = random.choice(address_data)['postcode']

    # Generate new values
    new_id = generate_random_id(existing_ids)
    location = generate_random_location()
    phone = generate_random_phone(existing_phones)
    name = generate_random_name(existing_names)

    # Create new restaurant entry
    new_restaurant = {
        "address": address,
        "area": area,
        "food": food,
        "id": new_id,
        "location": location,
        "name": name,
        "phone": phone,
        "postcode": postcode,
        "pricerange": pricerange,
        "type": "restaurant"
    }
    
    return new_restaurant

# Function to augment restaurants
def augment_restaurants(original_restaurants, factor):
    existing_ids = [restaurant['id'] for restaurant in original_restaurants]
    existing_phones = [restaurant['phone'] for restaurant in original_restaurants if "phone" in restaurant]
    existing_names = [restaurant['name'] for restaurant in original_restaurants]
    augmented_restaurants = copy.deepcopy(original_restaurants)
    
    # Create new restaurants
    for _ in range(len(original_restaurants) * (factor - 1)):
        new_restaurant = create_restaurant(original_restaurants, existing_ids, existing_phones, existing_names)
        augmented_restaurants.append(new_restaurant)
        existing_ids.append(new_restaurant['id']) 
        existing_phones.append(new_restaurant['phone']) 
        existing_names.append(new_restaurant['name']) 
    
    return augmented_restaurants

augmented_restaurants = augment_restaurants(original_restaurants, AUGM_SCALE)

write_json(augmented_restaurants, f"KB/restaurant_db_x{AUGM_SCALE}.json")
