from database import get_connection

def match_grocery_list(grocery_items):
    conn = get_connection()
    cursor = conn.cursor()

    # Get all selected stores
    cursor.execute('''
        SELECT s.id, s.name 
        FROM stores s
        JOIN user_stores us ON s.id = us.store_id
        WHERE us.selected = 1
    ''')
    stores = cursor.fetchall()

    results = []

    for store in stores:
        store_id = store[0]
        store_name = store[1]
        matched_items = []
        total_savings = 0

        for item in grocery_items:
            item = item.strip().lower()
            if not item:
                continue

            # Search promotions for this item in this store
            cursor.execute('''
                SELECT product_name, original_price, promo_price, discount
                FROM promotions
                WHERE store_id = ?
                AND LOWER(product_name) LIKE ?
            ''', (store_id, f'%{item}%'))

            matches = cursor.fetchall()

            for match in matches:
                original = match[1] or 0
                promo = match[2] or 0
                saving = original - promo if original > 0 else 0
                total_savings += saving
                matched_items.append({
                    "item_searched": item,
                    "product_found": match[0],
                    "original_price": original,
                    "promo_price": promo,
                    "discount": match[3],
                    "saving": round(saving, 2)
                })

        results.append({
            "store_id": store_id,
            "store_name": store_name,
            "matched_items": matched_items,
            "total_savings": round(total_savings, 2),
            "items_matched": len(matched_items)
        })

    conn.close()

    # Sort by total savings — best store first
    results.sort(key=lambda x: x["total_savings"], reverse=True)

    return results


def get_recommendation(grocery_items):
    results = match_grocery_list(grocery_items)

    if not results:
        return None

    best_store = results[0]

    return {
        "recommendation": best_store,
        "all_stores": results
    }