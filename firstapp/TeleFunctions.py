from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.types import InputFile, DocumentAttributeFilename, InputMessagesFilterDocument
from tqdm import tqdm
import os
import asyncio






def getmsg(api_id, api_hash, phone_number, group_name):
    with TelegramClient('session_name', api_id, api_hash) as client:
        entity = client.get_entity(group_name)
        getmessage = client.get_messages(entity)
        for message in client.iter_messages(entity.id, reverse=True):
            print(message.message)
            if not message.media:
                continue
            if message.photo:
                print('Photo:', message.photo)
            elif message.video:
                print('Video:', message.video)
            elif message.audio:
                print('Audio:', message.audio)
            elif message.document:
                print('Document:', message.document)
                file_name = None
                for attribute in message.document.attributes:
                    if isinstance(attribute, DocumentAttributeFilename):
                        file_name = attribute.file_name
                        break
                if file_name:
                    print(file_name)
                
            if message.file:
                print('File:', message.file)
    
# async def getmsg(api_id, api_hash, phone_number, group_name):
#     async with sync.AsyncTelegramClient('session_name', api_id, api_hash) as client:
#         entity = await client.get_entity(group_name)
#         async for message in client.iter_messages(entity.id, reverse=True):
#             print(message.message)    








# WORKING
def delete_files(api_id, api_hash, phone_number, group_name):
    # Connect to Telegram API
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()

    # Login
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))

    # Get the group entity
    entity = client.get_entity(group_name)

    # Get all the document messages in the group
    messages = client.get_messages(entity, filter=InputMessagesFilterDocument)
    
    # Delete each document message
    for message in client.iter_messages(entity.id, reverse=True):        
        client.delete_messages(entity, [message.id])

    # Disconnect from Telegram API
    client.disconnect()




# WORKING
async def a_upload_file(client, group_name, file_path, caption='', progress_callback=None):
    entity = await client.get_entity(group_name)
    result = await client.send_file(entity, file=file_path, caption=caption, progress_callback=progress_callback)
    return result


async def upload_files_parallel(api_id, api_hash, phone_number, group_name, file_paths, caption=''):
    # Connect to Telegram API
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone_number)

    # Get the total size of all files for progress tracking
    total_size = sum(os.path.getsize(file_path) for file_path in file_paths)

    with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
        def progress_callback(current, total):
            progress_bar.update(current - progress_callback.previous)
            progress_callback.previous = current

        progress_callback.previous = 0

        # Create the tasks to upload each file concurrently
        tasks = []
        for file_path in file_paths:
            task = asyncio.create_task(a_upload_file(client, group_name, file_path, caption, progress_callback))
            tasks.append(task)

        # Wait for all tasks to complete
        upload_results = await asyncio.gather(*tasks)

    await client.disconnect()
    return upload_results


def upload_multiple_files_with_progress(api_id, api_hash, phone_number, group_name, file_paths, caption=''):
    loop = asyncio.get_event_loop()
    upload_results = loop.run_until_complete(
        upload_files_parallel(api_id, api_hash, phone_number, group_name, file_paths, caption)
    )
    loop.close()
    return upload_results



# WORKING
def upload_file_with_progress(api_id, api_hash, phone_number, group_name, file_path, caption=''):
    # Connect to Telegram API
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Ensure the phone number is connected to the account
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code: '))

        # Get the file size for progress tracking
        file_size = os.path.getsize(file_path)
        
        # Upload the file with a progress bar
        with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
            def progress_callback(current, total):
                progress_bar.update(current - progress_callback.previous)
                progress_callback.previous = current

            progress_callback.previous = 0
            
            # Upload the file with the progress callback
            # entity = client.get_entity(group_name)
            entity = client.get_entity(group_name)
            result = client.send_file(entity, file=file_path, caption=caption, progress_callback=progress_callback)
        
        return result



# WORKING
def upload_file(api_id, api_hash, phone_number, group_name, file_path, caption=''):
    # Connect to Telegram API
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Ensure the phone number is connected to the account
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code: '))
        
        # Upload the file
        # entity = client.get_entity(group_name)
        entity = client.get_entity(group_name)
        result = client.send_file(entity, file=file_path, caption=caption)
        
        return result



# WORKING
def create_telegram_group(phone_number, group_title, group_participants, api_id=26537899, api_hash="809d4d7586d0e8b681cbcee8d40ae568"):
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set the new event loop as the current event loop

    # Connect to Telegram API
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Ensure the phone number is connected to the account
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code: '))        
        # Create a new group
        result = client(functions.messages.CreateChatRequest(
            title=group_title,
            users=group_participants
        ))
        # Get the created group ID
        group_name = result.chats[0].id        
        return group_name
# def create_telegram_group(phone_number, group_title, group_participants, api_id=26537899, api_hash="809d4d7586d0e8b681cbcee8d40ae568"):
#     # Connect to Telegram API
#     with TelegramClient('session_name', api_id, api_hash) as client:
#         # Ensure the phone number is connected to the account
#         client.connect()
#         if not client.is_user_authorized():
#             client.send_code_request(phone_number)
#             client.sign_in(phone_number, input('Enter the code: '))        
#         # Create a new group
#         result = client(functions.messages.CreateChatRequest(
#             title=group_title,
#             users=group_participants
#         ))
#         # Get the created group ID
#         group_name = result.chats[0].id        
#         return group_name


# WORKING
def delete_group(api_id, api_hash, phone_number, group_name):
    # Create a Telegram client
    client = TelegramClient('session_name', api_id, api_hash)

    # Connect to the Telegram API
    client.connect()

    # Check if the user is already authorized
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))

    # Get the group information
    chats = client.get_dialogs()
    group = next((c for c in chats if c.name == group_name and c.is_group), None)

    # Check if the group exists
    if group is None:
        print(f"The group '{group_name}' does not exist.")
    else:
        print("group exists")    

    entity = client.get_entity(group_name)  

    # Delete the group
    result = client(functions.messages.DeleteChatRequest(
        chat_id = entity.id
    ))
    print(result)

    print(f"The group '{group_name}' has been deleted.")

    # Disconnect the client
    client.disconnect()


# WORKING
def check_group(api_id, api_hash, phone_number, group_name):
    # Create a Telegram client
    client = TelegramClient('session_name', api_id, api_hash)

    # Connect to the Telegram API
    client.connect()

    # Check if the user is already authorized
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))

    # Get the group information
    chats = client.get_dialogs()
    group = next((c for c in chats if c.name == group_name and c.is_group), None)

    # Check if the group exists
    if group is None:
        print(f"The group '{group_name}' does not exist.")
    else:
        print(f"The group '{group_name}' exists.")


# WORKING
def rename_telegram_group(api_id, api_hash, phone_number, group_name,new_name):
    # Connect to Telegram API
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Ensure the phone number is connected to the account
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code: '))

        entity = client.get_entity(group_name)

    
        result = client(functions.messages.EditChatTitleRequest(
            chat_id=entity.id,
            title=new_name
        ))
        print(result.stringify())




