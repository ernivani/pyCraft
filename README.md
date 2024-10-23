# Minecraft-Like Game using Ursina Engine

This project is a Minecraft-like voxel game built using the [Ursina](https://www.ursinaengine.org/) engine. The game includes features like block textures, inventory management, terrain generation, and first-person movement controls.

## Features

- **Voxel-based world**: Build and destroy blocks in a procedurally generated terrain.
- **Custom Textures**: Blocks and inventory items are textured with custom assets.
- **Inventory System**: Switch between different block types for placement.
- **Procedural Terrain Generation**: Terrain heights are generated using Perlin noise.
- **First-Person Controller**: Move around the world in a first-person perspective.

## Installation

1. Clone this repository.
    ```bash
    git clone https://github.com/ernivani/pyCraft.git
    ```

2. Create a virtual environment.
    ```bash
    python -m venv .venv
    ```

3. Activate the virtual environment.

    - On Windows:
        ```bash
        .\.venv\Scripts\activate
        ```

    - On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4. Install the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```

5. Run the game.
    ```bash
    python main.py
    ```

## Project Structure

- `main.py`: The main game script.
- `Assets/`: Folder containing all textures, models, and sounds for the game.
- `requirements.txt`: A list of Python dependencies needed for the project.

## Controls

- **W/A/S/D**: Move
- **Mouse Scroll**: Switch between blocks in the inventory
- **1-9 Keys**: Select block slot
- **Left Mouse**: Destroy block
- **Right Mouse**: Place block

## Dependencies

- [Ursina Engine](https://www.ursinaengine.org/)
- [Perlin Noise](https://pypi.org/project/noise/)

## Assets

Assets such as block textures and sounds can be found in the `Assets` folder. The following block textures are included:

- Grass
- Stone
- Brick
- Dirt
- Wood

## License

This project is open-source and available under the MIT License.
