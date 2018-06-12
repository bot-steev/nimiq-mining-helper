import discord
import discord.utils
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import sys
import sqlite3
import datetime
import os
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

client = Bot(description="Nimiq Mining Helper",
             command_prefix="!", pm_help=False)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to ' +
          str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('You are running Nimiq-Mining-Helper[BETA]')
    print('Created by steev0#0420')
    return await client.change_presence(game=discord.Game(name='Stacking Bags 💰'))

sqlite_file = './src/miner_info_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

key_file = open('./src/key.txt', 'r')
if not key_file:
    print('File key.txt can\'t be found')
    sys.exit(0)

api_key = key_file.read().splitlines()[0]
if not api_key:
    print('No API key in discord_key.txt')
    sys.exit(0)

key_file.close()

async def server_heartbeat(message):
    await client.wait_until_ready()
    
    while not client.is_closed:
        
        await client.send_message(message.channel,'Starting Server Heartbeat Check ❤')
        
        cntr2 = 0

        ComputeEngine = get_driver(Provider.GCE)
                
        c.execute ('SELECT * from service_account')
        credentials_list = c.fetchall()
        for credentials in credentials_list:
            (account_name, file_path) = credentials
        
        c.execute ('SELECT * FROM project_info')
        project_list = c.fetchall()
        for project in project_list:
            (project_name,project_alias) = project
            driver = ComputeEngine(account_name, file_path, project=project_name)
            node_list = driver.list_nodes()
            await client.send_message (message.channel, 'Now Checking: ' + project_alias + '🔍')
            for node in node_list:
                if node.state == 'stopped' or node.state == 'terminated':
                    await client.send_message (message.channel, node.name + ' is dead 💀')
                    await client.send_message (message.channel, 'Firing start signal to: ' + node.name + '🚀')
                    start_node = driver.ex_start_node(node)
                    asyncio.sleep(20)
                    if start_node == True:
                        await client.send_message (message.channel, node.name + ' started successfully ✅')
                        cntr2 += 1
                    else:
                        await client.send_message (message.channel, 'Failed to start '+ node.name + '❌')
                elif node.state == 'running':
                    cntr2 += 1
                 
        await client.send_message(message.channel, str(cntr2) + ' servers are running optimally  💰')   
        await asyncio.sleep(120)

async def account_info(message):
    await client.wait_until_ready()
    c.execute('SELECT * FROM service_account')
    account_list = c.fetchall()
    if len(account_list) == 0:
        await client.send_message(message.channel, 'There are no service accounts currently in the Databse:')
    else:
        await client.send_message(message.channel, 'Current Service Accounts in the Database:')
        for account in account_list:
            (account_name,path_to_file) = account
            await client.send_message(message.channel, 'Service Account: ' + account_name + '\nPath to JSON file: ' + path_to_file)

async def add_account(message):
    await client.wait_until_ready()
    message_content = (message.content).split(' ')
    account_name = (message_content[1])
    path_to_file = (message_content[2])
    c.execute('INSERT INTO service_account VALUES(?,?)',(account_name, path_to_file))
    conn.commit()
    await client.send_message(message.channel, 'Service Account inserted into Database ✅')

async def delete_account(message):
    await client.wait_until_ready()
    message_content = (message.content).split(' ')
    account_name = (message_content[1])
    c.execute('DELETE FROM service_account WHERE account_name=(?)',(account_name))
    conn.commit()
    await client.send_message(message.channel, 'Service Account deleted from Database ✅')

async def project_list(message):
    await client.wait_until_ready()
    c.execute('SELECT * FROM project_info')
    project_list = c.fetchall()
    if len(project_list) == 0:
        await client.send_message(message.channel, 'There are no projects currently defined in the Database.')
    else:
        await client.send_message(message.channel, 'Current Projects in the Database')
        for project in project_list:
            (project_name, project_alias) = project
            await client.send_message(message.channel, 'Project ID: ' +project_name+ '\tProject Alias: ' + project_alias)

async def add_project(message):
    await client.wait_until_ready()
    message_content = (message.content).split(' ')
    project_name = (message_content[1])
    project_alias = (message_content[2])
    c.execute('INSERT INTO project_info VALUES(?,?)',(project_name, project_alias))
    conn.commit()
    await client.send_message(message.channel, 'Project Info inserted into Database ✅')

async def delete_project(message):
    await client.wait_until_ready()
    message_content = (message.content).split(' ')
    project_name = (message_content[1])
    c.execute('DELETE FROM project_info WHERE project_name=(?)',(project_name))
    conn.commit()
    await client.send_message(message.channel, 'Project Info deleted from Database ✅')

async def clear_database(message):
    await client.wait_until_ready()
    c.execute('DELETE FROM project_info')
    c.execute('DELETE FROM service_account')
    conn.commit()
    c.execute('SELECT * FROM service_account')
    service_info = c.fetchall()
    if len(service_info)>0:
        await client.send_message(message.channel, 'Failed to clear Service Account Table')
    else:
        await client.send_message(message.channel, 'Service Account Table Cleared.')
    c.execute('SELECT * FROM project_info')
    project_info = c.fetchall()
    if len(project_info)>0:
        await client.send_message(message.channel, 'Failed to clear Project Info Table')
    else:
        await client.send_message(message.channel, 'Project Info Table Cleared.')

@client.event
async def on_message(message):
    await client.wait_until_ready()
    
    if message.content.startswith('!check'):
        client.loop.create_task(server_heartbeat(message))
        await client.send_message(message.channel, 'Server Heartbeat Initialised')

    elif message.content.startswith('!accountinfo'):
        await account_info(message)

    elif message.content.startswith('!addaccount'):
        await add_account(message)
    
    elif message.content.startswith('!deleteaccount'):
        await delete_account(message)

    elif message.content.startswith('!projectinfo'):
        await project_list(message)

    elif message.content.startswith('!addproject'):
        await add_project(message)

    elif message.content.startswith('!deleteproject'):
        await delete_project(message)

    elif message.content.startswith('!cleardb'):
        await clear_database(message)
        
client.run(str(api_key))