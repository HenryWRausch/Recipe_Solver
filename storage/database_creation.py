import sqlite3
from config import config

configs = config.load_config('config/config.json')
conn = sqlite3.connect(configs.database_location)

tables = {
    'ingredients' : '''
    CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    );
    ''',

    'recipes' : '''
    CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    time INTEGER NOT NULL, -- minutes
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5)
    );
    ''',

    'recipe_ingredients' : '''
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    unit TEXT NOT NULL,

    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
    );
    '''
}

for table in tables.values():
    print(f'Attempting to create table: {table}')
    conn.execute(table)


conn.commit()
conn.close()