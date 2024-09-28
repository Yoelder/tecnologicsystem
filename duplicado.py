import json

# Cambia esto por la ruta de tu archivo JSON
input_file_path = 'datos.json'
output_file_path = 'datos_sin_duplicados.json'

def remove_duplicates(input_file, output_file):
    # Cargar datos desde el archivo JSON
    with open(input_file, 'r') as f:
        data = json.load(f)

    seen = set()  # Para almacenar entradas ya vistas
    unique_data = []  # Lista para almacenar datos únicos

    for entry in data:
        # Define una clave única para cada entrada
        key = (entry['model'], entry['pk'])  # (model, pk) como clave única
        
        if key not in seen:
            seen.add(key)
            unique_data.append(entry)

    # Guardar los datos únicos en un nuevo archivo JSON
    with open(output_file, 'w') as f:
        json.dump(unique_data, f, indent=4)

    print(f"Datos sin duplicados guardados en '{output_file}'")

if __name__ == "__main__":
    remove_duplicates(input_file_path, output_file_path)
