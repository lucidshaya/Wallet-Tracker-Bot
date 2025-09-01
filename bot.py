import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import asyncio
import re

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

# In-memory storage (replace with DB for production)
wallets = {}  # user_id: [list of addresses]
tracking_tasks = {}  # user_id: asyncio task

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to your Portfolio Tracker Bot! Use /addwallet <eth_address> to add a wallet, /balance to check, /track to start monitoring.')

async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if not context.args:
        await update.message.reply_text('Usage: /addwallet <eth_address>')
        return
    address = context.args[0]
    # Basic Ethereum address validation
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        await update.message.reply_text('Invalid Ethereum address format.')
        return
    if user_id not in wallets:
        wallets[user_id] = []
    if address not in wallets[user_id]:
        wallets[user_id].append(address)
        await update.message.reply_text(f'Added wallet: {address}')
    else:
        await update.message.reply_text(f'Wallet {address} already added.')

async def get_balance(address: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            # ETH balance
            eth_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
            eth_response = await client.get(eth_url)
            eth_data = eth_response.json()
            if eth_data['status'] != '1':
                return f"Error fetching ETH balance for {address}: {eth_data.get('message', 'Unknown error')}"
            eth_balance = int(eth_data['result']) / 10**18
            
            # Token balances (basic example; expand as needed)
            token_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
            token_response = await client.get(token_url)
            token_data = token_response.json()
            tokens = set(tx['tokenSymbol'] for tx in token_data.get('result', [])) if token_data['status'] == '1' else set()
            
            return f"ETH Balance: {eth_balance:.4f} ETH\nTokens: {', '.join(tokens) or 'None'}"
    except Exception as e:
        logger.error(f"Error fetching balance for {address}: {e}")
        return f"Error fetching data for {address}. Try again later."

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in wallets or not wallets[user_id]:
        await update.message.reply_text('No wallets added. Use /addwallet first.')
        return
    message = 'Your Portfolio:\n'
    for addr in wallets[user_id]:
        # Directly await get_balance since it's now async
        balance_info = await get_balance(addr)
        message += f"\nWallet {addr}:\n{balance_info}\n"
    await update.message.reply_text(message)

async def monitor_wallet(context: ContextTypes.DEFAULT_TYPE, user_id: int, chat_id: int) -> None:
    while True:
        for addr in wallets.get(user_id, []):
            balance_info = await get_balance(addr)
            if 'Error' not in balance_info:
                await context.bot.send_message(chat_id=chat_id, text=f"Update for {addr}:\n{balance_info}")
        await asyncio.sleep(60)  # Poll every 60s; use webhooks for efficiency

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    if user_id in tracking_tasks:
        await update.message.reply_text('Tracking already running.')
        return
    task = asyncio.create_task(monitor_wallet(context, user_id, chat_id))
    tracking_tasks[user_id] = task
    await update.message.reply_text('Started tracking your wallets. Updates every 60s.')

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addwallet", add_wallet))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("track", track))
    application.run_polling()

if __name__ == '__main__':
    main()