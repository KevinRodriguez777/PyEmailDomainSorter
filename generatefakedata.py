from faker import Faker
import os, time


def main():
    startTime = time.time()
    faker = Faker()
    with open("temp.txt", "a+") as f:
        f.writelines(f"{faker.email(safe=True)}\n" for i in range(10000000))

    executionTime = time.time() - startTime

    print(executionTime)


if __name__ == "__main__":
    main()
