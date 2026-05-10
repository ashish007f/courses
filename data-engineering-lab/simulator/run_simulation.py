import httpx
import asyncio
import random
import time
from uuid import UUID

API_URL = "http://localhost:8000"

async def run_simulation():
    async with httpx.AsyncClient() as client:
        print("Starting Banking Simulation...")
        
        while True:
            try:
                # 1. Simulate New Customer
                cust_resp = await client.post(f"{API_URL}/customers/simulate")
                customer_resp_data = cust_resp.json()
                if cust_resp.status_code != 200:
                    print(f"Error creating customer: {customer_resp_data}")
                    await asyncio.sleep(2)
                    continue

                customer = customer_resp_data["customer"]
                customer_id = customer["id"]
                print(f"Created Customer: {customer_id}")

                # 2. Create Account for Customer
                acc_resp = await client.post(f"{API_URL}/accounts/{customer_id}")
                account_resp_data = acc_resp.json()
                if acc_resp.status_code != 200:
                    print(f"Error creating account: {account_resp_data}")
                    await asyncio.sleep(2)
                    continue
                
                account = account_resp_data["account"]
                account_id = account["id"]
                print(f"  Created Account: {account_id}")

                # 3. Simulate multiple transactions for this account
                for _ in range(random.randint(2, 6)):
                    amount = round(random.uniform(10.0, 500.0), 2)
                    txn_resp = await client.post(f"{API_URL}/transactions/deposit/{account_id}?amount={amount}")
                    if txn_resp.status_code == 200:
                        txn_data = txn_resp.json()
                        txn = txn_data["transaction"]
                        print(f"    Processed Deposit: {txn['amount']} (New Balance: {txn_data['new_balance']})")
                    else:
                        print(f"    Error processing transaction: {txn_resp.text}")
                    await asyncio.sleep(random.uniform(0.2, 0.8))

                await asyncio.sleep(random.uniform(2.0, 5.0))

            except Exception as e:
                print(f"Error in simulation loop: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    # Wait for API to be ready
    print("Simulation script waiting for API to start...")
    asyncio.run(run_simulation())
