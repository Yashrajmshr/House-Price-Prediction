import pandas as pd
import numpy as np
import random
import os

def generate_house_data(num_samples=50000):
    city_base_rates = {
        'Mumbai': 14000,
        'Bengaluru': 9500,
        'Delhi-NCR': 9200,
        'Hyderabad': 7000,
        'Pune': 5000
    }
    
    locality_tiers = {
        'Premium': 1.6,
        'Mid-segment': 1.1,
        'Affordable': 0.85
    }
    
    property_types = {
        'Apartment': 1.0, 
        'Independent House': 1.25, 
        'Villa': 1.5
    }
    
    furnishing_status = {
        'Unfurnished': 1.0, 
        'Semi-Furnished': 1.05, 
        'Furnished': 1.15
    }
    
    status_types = {
        'Ready to move': 1.1, 
        'Under Construction': 0.9
    }

    data = []
    
    cities = list(city_base_rates.keys())
    loc_tiers = list(locality_tiers.keys())
    prop_types = list(property_types.keys())
    furnish_types = list(furnishing_status.keys())
    stat_types = list(status_types.keys())
    
    for _ in range(num_samples):
        city = random.choice(cities)
        tier = random.choices(loc_tiers, weights=[0.2, 0.6, 0.2])[0]
        prop_type = random.choices(prop_types, weights=[0.8, 0.15, 0.05])[0]
        furnish = random.choice(furnish_types)
        status = random.choice(stat_types)
        
        bhk = random.choices([1, 2, 3, 4, 5], weights=[0.2, 0.4, 0.3, 0.08, 0.02])[0]
        
        if bhk == 1:
            area = random.randint(350, 600)
        elif bhk == 2:
            area = random.randint(650, 1200)
        elif bhk == 3:
            area = random.randint(1250, 2000)
        elif bhk == 4:
            area = random.randint(2100, 3500)
        else:
            area = random.randint(3600, 6000)
            
        bathrooms = max(1, min(bhk + random.choice([0, 1, -1]), bhk + 2))
        balcony = random.choice([0, 1, 2, 3])
        if bhk == 1:
            balcony = random.choice([0, 1])
            
        base_rate = city_base_rates[city]
        
        rate = base_rate * locality_tiers[tier] * property_types[prop_type] * furnishing_status[furnish] * status_types[status]
        
        price = area * rate
        
        # Add random noise (+/- 5 to 15%) to make dataset realistic (so ML model isn't just learning a perfect math formula)
        noise = random.uniform(0.85, 1.15)
        final_price = price * noise
        
        # Convert to nearest thousands
        final_price = round(final_price, -3)
        
        age_of_property = 0 if status == 'Under Construction' else random.randint(0, 20)
        
        data.append({
            'City': city,
            'Locality_Tier': tier,
            'Property_Type': prop_type,
            'Furnishing_Status': furnish,
            'Status': status,
            'BHK': bhk,
            'Area_SqFt': area,
            'Bathrooms': bathrooms,
            'Balcony': balcony,
            'Age_of_Property': age_of_property,
            'Price': final_price
        })
        
    df = pd.DataFrame(data)
    
    df['Price_Lakhs'] = df['Price'] / 100000.0
    df['Price_Lakhs'] = df['Price_Lakhs'].round(2)
    
    output_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset generated successfully with {num_samples} rows -> {output_path}")

if __name__ == "__main__":
    generate_house_data(50000)
