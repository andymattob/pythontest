import numpy as np
import matplotlib.pyplot as plt

def generate_stone_texture(size=(512, 512)):
    # Skapar ett brusmönster för sten genom att kombinera slumpmässigt brus
    noise = np.random.rand(*size)
    for i in range(1, 5):
        # Förskjutning och skalning för att simulera fraktalt brus
        noise += np.roll(noise, i, axis=0) * 0.5**i
        noise += np.roll(noise, i, axis=1) * 0.5**i
    
    # Normalisera värdena mellan 0 och 1
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    
    # Spara som bild med gråskala
    plt.imshow(noise, cmap='gray')
    plt.axis('off')
    plt.savefig('/ark_img/stone.png', bbox_inches='tight', pad_inches=0)
    plt.close()
    return '/ark_img/stone.png'

def generate_wood_texture(size=(512, 512)):
    # Skapar trämönster med hjälp av en sinusvåg och lätt brus
    x = np.linspace(0, 10, size[0])
    y = np.linspace(0, 10, size[1])
    X, Y = np.meshgrid(x, y)
    
    # Grundmönster (ådring)
    grain = np.sin(X * 2 + np.random.normal(0, 0.5, size))
    
    # Lägg till brus för att det ska se mer naturligt ut
    noise = np.random.normal(0, 0.1, size)
    wood = grain + noise
    
    # Normalisera
    wood = (wood - wood.min()) / (wood.max() - wood.min())
    
    # Använd en koppar/brun färgskala för trä
    plt.imshow(wood, cmap='copper')
    plt.axis('off')
    plt.savefig('/ark_img/wood.png', bbox_inches='tight', pad_inches=0)
    plt.close()
    return '/ark_img/wood.png'

# Generera texturerna
stone_file = generate_stone_texture()
wood_file = generate_wood_texture()

print(f"Texturer sparade som: {stone_file} och {wood_file}")