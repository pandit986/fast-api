# import time

# print("=" *40,"\n")
# print("code 1")

# def download_file(file_number):
#     print(f"downloading file {file_number}...")
#     time.sleep(2)
#     print(f"file {file_number} downloaded!")

# start = time.time()

# download_file(1)
# download_file(2)
# download_file(3)

# end = time.time()

# print(f"Total time taken: {end - start:.2f} seconds")
# print("\n" + "=" *40)

import asyncio
import time

async def download_file(file_number):
    print(f"downloading file {file_number}...")
    # not blocking the event loop, so other tasks can run while waiting
    await asyncio.sleep(2)
    print(f"file {file_number} downloaded!")
    return file_number

# async def main():
#     start = time.time()


#     # run task concurrently
#     task1 = asyncio.create_task(download_file(1))
#     task2 = asyncio.create_task(download_file(2))
#     task3 = asyncio.create_task(download_file(3))

#     await task1
#     await task2 
#     await task3

#     end = time.time()
#     print(f"Total time taken: {end - start:.2f} seconds")


# asyncio.run(main())

async def main():
    start = time.time()

    # run task concurrently
    results = await asyncio.gather(
        download_file(1),
        download_file(2),
        download_file(3)
    )
    print(f"Results: {results}")
    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")

asyncio.run(main())


