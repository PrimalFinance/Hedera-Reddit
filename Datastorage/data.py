
import os
import csv




class NetworkData:
    def __init__(self, filename: str = "/home/pi/Hedera-Reddit/Database/network_tracking.csv"):
        self.filename = filename
        self.fieldnames = ["Date", "Time",
                           "Mainnet Transactions", "Mainnet TPS",
                           "Testnet Transactions", "Testnet TPS",
                           "Price", "Marketcap", "Rank","TVL", "Accounts", "inBTC"]

     '''------------------------- Create file handling'''
    def create_file(self): 
        with open(self.filename, mode='w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
            writer.writeheader()
    
    def insert_data(
                    self, date: str, time: str, main_txn: int,
                    main_tps: int, test_txn: int, test_tps: int,
                    price: float, marketcap: int, rank: int, tvl: int,
                    accounts: int, inBTC: float
                    ) -> None:
        
        '''
        - Take data from the webscraper and insert it into the csv file.  

        :param date: The date of the recording in UTC.
        :param time: The time of the recording in UTC. 
        :param main_txn: The number of total transaction on the Hedera mainnet at the time of the record.
        :param main_tps: The transactions-per-second on the mainnet at the time of the record.
        :param test_txn: The number of total transactions on the Hedera testnet at the time of the record.
        :param test_tps: The transactions-per-second on the testnet at the time of the record.
        :param price: The price of HBAR at the time of the record. 
        :param marketcap: The marketcap at the time of the record.
        :param rank: The ranking of marketcap relative to other cryptocurrencies.
        :param tvl: The total value locked on the Hedera network. 
        :param accounts: The number of accounts on the Hedera network. 
        :param inBTC: The value of HBAR in terms of BTC. 
        :return: None
        '''
        headers_exist = self._check_headers()
        if not headers_exist:
            self.create_file()
        with open(self.filename, mode='a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
            writer.writerow({"Date": date,
                            "Time": time,
                            "Mainnet Transactions": main_txn,
                            "Mainnet TPS": main_tps,
                            "Testnet Transactions": test_txn,
                            "Testnet TPS": test_tps,
                            "Price": price,
                            "Marketcap": marketcap,
                            "Rank": rank,
                            "TVL": tvl,
                            "Accounts":accounts})
            

        '''
        :param : 
        :return:
        '''
        
        '''
        :param : 
        :return:
        '''
        
        '''
        :param : 
        :return:
        '''
        
        '''
        :param : 
        :return:
        '''
        
        '''
        :param : 
        :return:
        '''
        
        '''
        :param : 
        :return:
        '''