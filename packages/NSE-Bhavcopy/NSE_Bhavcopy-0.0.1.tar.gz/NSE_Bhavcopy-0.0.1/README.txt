The Library downloads daily Bhavcopy data for equity, index, and derivatives from the National Stock Exchange (NSE) of India and saves the data in a single storage location. If the main file already exists, the code will resume downloading data from the last date in the file until it reaches the end date.

# Define start and end dates, and convert them into date format
startDate = datetime.date(2023, 3, 1)
endDate = datetime.date(2023, 3, 10)
wait_time = random.randint(1,2) # wait time in seconds to avoid getting blocked

# Create an instance of the NseDataExtractor class and call the nse_equity_bhavcopy() method
nse = NSE_Bhavcopy(startDate, endDate, data_storage, wait_time)

nse.nse_equity_bhavcopy()
nse.nse_derivative_bhavcopy()
nse.nse_index_bhavcopy()
