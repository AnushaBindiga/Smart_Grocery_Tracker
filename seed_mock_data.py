from database import get_connection
from datetime import date

def seed_mock_promotions():
    conn = get_connection()
    cursor = conn.cursor()
    
    today = str(date.today())
    
    # Get store IDs
    cursor.execute("SELECT id, name FROM stores")
    stores = {row[1]: row[0] for row in cursor.fetchall()}
    
    mock_data = {
        "Lidl": [
            ("Lait demi-écrémé 1L x6", 4.99, 3.99, "-20%"),
            ("Poulet entier fermier", 8.99, 6.99, "-22%"),
            ("Pâtes spaghetti 500g", 1.29, 0.89, "-31%"),
            ("Yaourt nature x8", 2.49, 1.79, "-28%"),
            ("Jus d'orange 1L", 2.19, 1.49, "-32%"),
            ("Beurre doux 250g", 3.49, 2.69, "-23%"),
            ("Fromage râpé 200g", 2.99, 2.19, "-27%"),
            ("Coca-Cola 1.5L", 2.29, 1.69, "-26%"),
            ("Céréales muesli 750g", 3.99, 2.99, "-25%"),
            ("Thon en boîte x4", 4.49, 3.29, "-27%"),
        ],
        "Super U": [
            ("Pain de mie complet", 1.99, 1.49, "-25%"),
            ("Œufs fermiers x12", 3.99, 2.99, "-25%"),
            ("Huile d'olive 75cl", 6.99, 4.99, "-29%"),
            ("Riz basmati 1kg", 2.99, 1.99, "-33%"),
            ("Café moulu 250g", 4.49, 3.29, "-27%"),
            ("Lessive liquide 2L", 7.99, 5.99, "-25%"),
            ("Bananes 1kg", 1.99, 1.29, "-35%"),
            ("Jambon blanc x4", 3.49, 2.49, "-29%"),
            ("Eau minérale 6x1.5L", 3.99, 2.79, "-30%"),
            ("Chocolat noir 100g", 1.79, 1.19, "-34%"),
        ],
        "E.Leclerc": [
            ("Steak haché 5% 4x100g", 5.99, 4.49, "-25%"),
            ("Saumon fumé 4 tranches", 4.99, 3.49, "-30%"),
            ("Fromage brie 200g", 3.29, 2.29, "-30%"),
            ("Tomates cerises 250g", 2.49, 1.69, "-32%"),
            ("Biscuits Lu 300g", 2.99, 1.99, "-33%"),
            ("Shampooing 400ml", 4.99, 3.49, "-30%"),
            ("Lait entier 1L x6", 5.49, 3.99, "-27%"),
            ("Pommes golden 1kg", 2.29, 1.59, "-31%"),
            ("Dentifrice x2", 3.99, 2.79, "-30%"),
            ("Soupe tomate 1L", 1.99, 1.39, "-30%"),
        ],
        "Intermarché": [
            ("Escalope de dinde 500g", 6.99, 4.99, "-29%"),
            ("Camembert 250g", 2.99, 1.99, "-33%"),
            ("Farine de blé 1kg", 1.49, 0.99, "-34%"),
            ("Sucre en poudre 1kg", 1.99, 1.39, "-30%"),
            ("Confiture fraises 370g", 2.49, 1.69, "-32%"),
            ("Pizza margherita 400g", 3.99, 2.79, "-30%"),
            ("Chips nature 150g", 2.29, 1.59, "-31%"),
            ("Gel douche 400ml", 3.49, 2.39, "-31%"),
            ("Carottes 1kg", 1.49, 0.99, "-34%"),
            ("Filets de cabillaud 300g", 5.99, 4.29, "-28%"),
        ]
    }
    
    for store_name, products in mock_data.items():
        store_id = stores.get(store_name)
        if not store_id:
            continue
            
        # Clear existing mock data for this store
        cursor.execute(
            "DELETE FROM promotions WHERE store_id = ?", (store_id,)
        )
        
        for product in products:
            cursor.execute('''
                INSERT INTO promotions 
                (store_id, product_name, original_price, promo_price, discount, date_scraped)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (store_id, product[0], product[1], 
                  product[2], product[3], today))
        
        print(f"Added {len(products)} mock promotions for {store_name}!")
    
    conn.commit()
    conn.close()
    print("\nAll mock data seeded successfully!")

if __name__ == "__main__":
    seed_mock_promotions()