from img_builder import run_by_json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = input()           # Pega o caminho do arquivo json (não funciona passando como argumento pro terminal)
    img = run_by_json(path)  # Retorna a imagem a partir dos valores do cmd

    # Salva a imagem resultante no arquivo output.png
    plt.imsave("output.png",img,format="png")
    
    print()
    print("Imagem gerada com sucesso")

    # Plota a imagem resultante    
    plt.imshow(img)
    plt.show()
