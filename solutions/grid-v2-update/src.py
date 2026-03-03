import csv

# 1. Beolvassuk a query-t a beépített, szupergyors csv modullal
# Ekkor dől el, hogy elindítjuk-e a nehézgépeket (Pandas/NumPy)
with open("query.csv", "r", encoding="utf-8") as f:
    queries = list(csv.DictReader(f))

num_queries = len(queries)

# --- DÖNTÉSI LOGIKA ---
if num_queries <= 50:
    # === GYORS ÁG (A grid_new-ból ismert (a-b)^2 logika) ===
    # Itt SEMMILYEN külső csomagot nem töltünk be a sebesség érdekében!
    
    with open("input.csv", "r", encoding="utf-8") as f:
        raw_movies = list(csv.DictReader(f))
    
    # Előkészítjük a filmeket (b^2 kiszámolása futásidőben)
    movies = []
    for m in raw_movies:
        mx, my = float(m['x']), float(m['y'])
        movies.append({
            'title': m['title'], 'id': m['imdb_id'], 
            'x': mx, 'y': my, 
            'm_sq': mx*mx + my*my # b^2 tag
        })
    
    geciskalacs = []
    for q in queries:
        qx, qy = float(q['x']), float(q['y'])
        q_sq = qx*qx + qy*qy # a^2 tag
        
        dists = []
        for m in movies:
            # d^2 = a^2 + b^2 - 2ab
            d2 = q_sq + m['m_sq'] - 2 * (qx * m['x'] + qy * m['y'])
            dists.append((d2, m['title'], m['id']))
        
        dists.sort()
        res = [dists[0][1], dists[0][2], dists[1][1], dists[1][2], dists[2][1], dists[2][2]]
        geciskalacs.append(res)
        
    # Mentés a beépített csv íróval - így a kicsiknél garantáltan nincs Pandas overhead
    with open("out.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["top1_title", "top1_id", "top2_title", "top2_id", "top3_title", "top3_id"])
        writer.writerows(geciskalacs)

else:
    # === GRID ÁG (A Grid-v2 vektorizált NumPy logikája) ===
    # A lassú csomagokat CSAK ITT töltjük be!
    import pandas as pd
    import numpy as np
    import json
    import pickle

    # 1. Lekérdezések átalakítása NumPy tömbbé
    query_df = pd.DataFrame(queries)
    q_x = query_df['x'].astype(float).values
    q_y = query_df['y'].astype(float).values

    # 2. Grid paraméterek betöltése
    with open('grid_params.json', 'r') as f:
        params = json.load(f)
    n, x_min, x_max, y_min, y_max = params['n'], params['x_min'], params['x_max'], params['y_min'], params['y_max']
    x_step, y_step = (x_max - x_min) / n, (y_max - y_min) / n

    # 3. Pickle adatok betöltése
    with open('grid_arrays.pkl', 'rb') as f:
        arrays = pickle.load(f)

    imdb_arr, title_arr = arrays['imdb_ids'], arrays['titles']
    x_arr, y_arr = arrays['x_coords'], arrays['y_coords']

    # 4. VEKTORIZÁCIÓ: Grid indexek kiszámítása egyszerre az összes query-re
    i_indices = np.clip(((q_x - (x_min + x_step / 2)) / x_step).astype(int), 0, n - 1)
    j_indices = np.clip(((q_y - (y_min + y_step / 2)) / y_step).astype(int), 0, n - 1)
    grid_idxs = i_indices * n + j_indices

    # 5. Végrehajtási ciklus
    geciskalacs = []
    for k in range(num_queries):
        qx, qy, idx = q_x[k], q_y[k], grid_idxs[k]
        
        cell_x, cell_y = x_arr[idx], y_arr[idx]
        cell_titles, cell_imdbs = title_arr[idx], imdb_arr[idx]
        
        # JAVÍTÁS: Ha üres a cella, akkor is adunk hozzá egy üres sort, hogy megmaradjon a darabszám!
        if len(cell_imdbs) == 0:
            geciskalacs.append([""] * 6)
            continue
        
        # Vektorizált távolság: d^2 = (qx-mx)^2 + (qy-my)^2
        dx, dy = cell_x - qx, cell_y - qy
        dists = dx * dx + dy * dy
        
        top_indices = np.argsort(dists)[:3]
        
        result = []
        for inner_idx in top_indices:
            result.extend([cell_titles[inner_idx], cell_imdbs[inner_idx]])
        
        while len(result) < 6: result.append("")
        geciskalacs.append(result)

    # 6. Mentés Pandas-szal - itt már úgyis betöltöttük, használhatjuk bátran
    out = pd.DataFrame(geciskalacs, columns=["top1_title", "top1_id", "top2_title", "top2_id", "top3_title", "top3_id"])
    out.to_csv("out.csv", index=False)