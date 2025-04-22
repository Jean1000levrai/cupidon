# hehe
# c'est un endroit pour test t pas obligé de le garder isidore
import time




def main():

    """Print the latest tutorial from Real Python"""

    tic = time.perf_counter()

    for i in range(10000):
        i +=1

    toc = time.perf_counter()

    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")




if __name__ == "__main__":

    main()