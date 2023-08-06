#******************************************************************************
#*
#* Wrapping relevant EnvisionRisk Market Risk-as-a-Service API calls into 
#* Python functions
#*
#******************************************************************************
#* The functionality wraps the EnvisionRisk market Risk-as-a-Service API into Python
#* style functions. The functions take familiar Python data objects as input, manage
#* the communication with the cloud server, and transform the JSON output
#* from the API into Python data structures.

import requests
import json
import os
import datetime
import maskpass
import pandas as pd
from typing import Dict
from queue import Empty

#******************************************************************************
#### General API Functions - GET/POST                                      ####
#******************************************************************************
# Base URL for API calls
API_URL = 'https://api.envisionrisk.com/v1/themis/'

def get_api_url(end_point):
    """ Internal function
    Generates the full API URL for a given endpoint."""
    return API_URL + end_point

def envrsk_post(access_token, url, body, params):
    """ Internal function
    Function to make a POST request to an API.

    This function sends a POST request to the specified API URL.
    It requires an access token, a URL, a body for the POST request,
    and a dictionary of query parameters. It adds the access token to the
    headers of the request and sends the POST request using the 'requests' library.

    Parameters:
        access_token (str): A string containing the access token.
        url (str): A string containing the URL of the API endpoint.
        body (dict): A dictionary containing the body of the POST request.
        params (dict): A dictionary containing the query parameters for the POST request.

    Returns:
        A dictionary containing the status code and the content of the API response.
    """
    
    # headers
    headers = {'ACCESS-TOKEN': access_token, 'Content-Type': 'application/json'}

    # Body
    body = json.dumps(body)

    # post call to the endpoint
    res = requests.post(url, params=params, headers=headers, data=body)

    return {'status_code': res.status_code, 'content': res.json()}

def envrsk_get(access_token, url, params):
    """ Internal function
    Function to make a GET request to an API.

    This function sends a GET request to the specified API URL.
    It requires an access token, a URL, and a dictionary of query parameters.
    It adds the access token to the headers of the request and sends
    the GET request using the 'requests' package.

    Args:
        access_token (str): A string containing the access token.
        url (str): A string containing the URL of the API endpoint.
        params (dict): A dictionary containing the query parameters for the GET request.

    Returns:
        A dictionary containing the status code and the content of the API response.
    """
    headers = {
        'ACCESS-TOKEN': access_token,
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers, params=params)
    return {'status_code': response.status_code, 'content': response.json()}

#******************************************************************************
#### Authentication                                                        ####
#******************************************************************************
def get_access_token():
    """ Internal function
    Retrieves the access token from environment variables."""    
    auth_flow_response = envrsk_auth_renew_access_token()
        
    if auth_flow_response["status-code"] == 200:        
        return os.getenv("ACCESS_TOKEN")
    else:
        raise Exception(auth_flow_response)

def envrsk_auth_renew_access_token(force_renew=False):
    """ Internal function
    Function to renew access token for API authentication.
    
    Renews the access token needed for API authentication. If force_renew 
    is True, a new token is retrieved even if the current one is still valid. 
    If user ID and password are available in the system environment variables, 
    they are used to get a new access token. If the current access token exists 
    and has not expired, it is used unless force_renew is True.

    Args:
        force_renew: A boolean value indicating whether to force the renewal
                     of the access token. Default is False.

    Returns:
        A message indicating the validity of the access token or any error message.
    """          

    if force_renew:
        envrsk_auth_log_out()
        return envrsk_auth_log_in_interactively()
    else:
        # Note: You should catch the exception when the ACCESS_TOKEN_EXPIRY is not a valid datetime
        if os.getenv("LOGGED_IN") != 'Yes' or os.getenv("ACCESS_TOKEN_EXPIRY") is None or os.getenv("ACCESS_TOKEN_EXPIRY") == str() or os.getenv("ACCESS_TOKEN") is None or os.getenv("ACCESS_TOKEN") == str():
            cond = True
        else:
            cond = datetime.datetime.strptime(os.getenv("ACCESS_TOKEN_EXPIRY"), '%Y-%m-%d %H:%M:%S') < datetime.datetime.now()
                        
        if cond:
            if not (os.getenv("LOGGED_IN") != 'Yes' or os.getenv("USR_ID") is None or os.getenv("USR_ID") == str() or os.getenv("USR_PWD") is None or os.getenv("USR_PWD") == str()):
                envrsk_auth_log_in(os.getenv("USR_ID"), os.getenv("USR_PWD"))                        
            else:          
                envrsk_auth_log_out()
                return envrsk_auth_log_in_interactively()              
        else:
            return {"status-code": 200, "message": "access-token is valid until: {}".format(os.getenv("ACCESS_TOKEN_EXPIRY"))}

def envrsk_auth_log_in(usr_id: str, usr_pwd: str):
    """     
    Function to get access token for API authentication
    
    This function obtains an access token needed for API authentication.
    It requires a user ID and password, and sends a GET request to the
    specified URL to retrieve the access token. If the request is successful,
    it sets the expiry time for the access token to 24 hours from the current time.

    Parameters:
    usr_id: str - A string containing the user ID.
    usr_pwd: str - A string containing the user password.

    Returns:
    A dictionary containing the status code, the access token and its expiry time.
    In case of error, it returns the error message.

    Example:
    token = envrsk_auth_log_in(usr_id = "your_user_id",
                               usr_pwd = "your_password")
    """
    # Check user input
    if usr_id is None or usr_id == str():
        return {"status-code": 400, "message": "Missing required parameter: usr_id"}

    if usr_pwd is None or usr_pwd == str():
        return {"status-code": 400, "message": "Missing required parameter: usr_pwd"}

    # Query parameters
    params = {"usr_id": usr_id, "usr_pwd": usr_pwd}

    # Send request
    response = requests.get("https://api.envisionrisk.com/auth/get-access-token", params=params)

    if response.status_code != 200:
        return response    
    
    # Calculate token expiry time and set the environment variables
    access_token_expiry = (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    os.environ["USR_ID"] = usr_id
    os.environ["USR_PWD"] = usr_pwd
    os.environ["ACCESS_TOKEN"] = response.json()
    os.environ["ACCESS_TOKEN_EXPIRY"] = access_token_expiry
    os.environ["LOGGED_IN"] = 'Yes'
    return {"status-code": 200, "message": "access-token has been acquired. You are now logged in. Happy coding!"}

def envrsk_auth_log_in_interactively():
    """ 
    Function to set access token for API authentication.
    
    Sets the environment variables for user ID and password, and retrieves 
    an access token for API authentication. It uses the user's input for the 
    email and password as credentials for authentication. The access token 
    retrieved is stored in the ACCESS_TOKEN environment variable.

    Returns:
        dict: A dictionary with status code and a corresponding message.
    
    Provide credentials - email and password. In case you have not yet received
    your personal credentials, contact EnvisionRisk at support@envisionrisk.com 
    """
    
    os.environ["USR_ID"] = input("Please provide email: ")       
    os.environ["USR_PWD"] = input("Please provide password: ")

    return envrsk_auth_log_in(os.getenv("USR_ID"), os.getenv("USR_PWD"))
    
def envrsk_auth_log_out():
    """ 
    Function to log out from the API.

    This function logs out from the API by removing the environment variables used.

    Examples:
        envrsk_auth_log_out()
    """
    os.environ["LOGGED_IN"] = 'No'
    os.environ["USR_ID"] = str()
    os.environ["USR_PWD"] = str()
    os.environ["ACCESS_TOKEN"] = str()
    os.environ["ACCESS_TOKEN_EXPIRY"] = str()

#******************************************************************************
#### Portfolio Functions                                                   ####
#******************************************************************************
def envrsk_portfolio_risk_regular(date: datetime.date, positions: pd.DataFrame, base_cur: str = None, horizon = None, signif_level = None, volatility_id = None, report_depth = None, simplify = False):
    """
    Function for estimating portfolio risk - Value-at-Risk (VaR) and Expected Shortfall (ES).

    This function uses the 'portfolio-risk-regular' API endpoint to estimate
    portfolio risk. It requires a date and a list of positions. It optionally takes in a base currency, 
    a horizon, a significance level, a volatility ID, a report depth, and a flag to simplify the output.

    Parameters:
    date (str): A date for which the portfolio risk should be estimated.
    positions (list): A list of positions in the portfolio.
    base_cur (str, optional): An optional base currency for the portfolio. Defaults to None.
    horizon (int, optional): An optional time horizon for the risk estimate. Defaults to None.
    signif_level (float, optional): An optional significance level for the risk measure. Defaults to None.
    volatility_id (str, optional): An optional volatility ID. Defaults to None.
    report_depth (int, optional): An optional depth of the report. Defaults to None.
    simplify (bool, optional): A flag indicating whether to simplify the output. Defaults to False.

    Value at Risk (VaR) is a statistical measure that estimates the maximum potential
    loss over a specified time horizon at a given confidence level. Expected
    Shortfall (ES), also known as Conditional Value at Risk (CVaR), estimates the
    average loss in the event that the VaR is exceeded. Both are forward-looking
    as they use statistical analysis based on historical data and volatility to
    predict potential future losses. They are essential for market risk management,
    helping organizations understand their risk exposure and potential financial
    impact under adverse market conditions.

    Returns:
    dict: A processed portfolio return value.

    Examples:
    positions = pd.DataFrame({"symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
                  "position_type": ["single_stock", "single_stock", "cash", "etf"],
                  "quantity": [129, 768, 69000, 89]})
    result_1 = envrsk_portfolio_risk_regular(
        date = "2022-12-31", 
        positions = positions)     
    
    result_2 = envrsk_portfolio_risk_regular(
        date = "2022-12-31",
        positions = positions,
        base_cur = "USD",
        horizon = 1,
        signif_level = 0.975,
        volatility_id = "point_in_time",
        report_depth = 0,
        simplify = True)
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-risk-regular"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "report_depth": report_depth
        }
        params = {k: v for k, v in params.items() if v is not None}
        if positions == pd.DataFrame():
            positions_dict = pd.DataFrame(positions).to_dict('list')
        else:
            positions_dict = positions

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_risk_component(date, positions, base_cur=None, horizon=None, 
                                     signif_level=None, volatility_id=None, 
                                     report_depth=None, simplify=False):
    """
    Function for estimating risk components of a portfolio

    This function uses the 'portfolio-risk-regular' API endpoint to estimate
    portfolio risk. It requires an access token and a date, along with a
    list of positions. It optionally takes in a base currency, a horizon,
    a significance level, a volatility ID, a report depth, and a flag
    to simplify the output.

    Parameters:
    date (str): A date for which the portfolio risk should be estimated.
    positions (DataFrame): A DataFrame of positions in the portfolio.
    base_cur (str, optional): An optional base currency for the portfolio. Default is None.
    horizon (int, optional): An optional time horizon for the risk estimate. Default is None.
    signif_level (float, optional): An optional significance level for the risk measure.
        Default is None.
    volatility_id (str, optional): An optional volatility ID. Default is None.
    report_depth (int, optional): An optional depth of the report. Default is None.
    simplify (bool, optional): A flag indicating whether to simplify the output. Default is False.

    Returns:
    DataFrame: A processed portfolio return value.

    Examples:    
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })
    result_1 = envrsk_portfolio_risk_component(
        date="2022-12-31", 
        positions=positions)

    result_2 = envrsk_portfolio_risk_component(
        date="2022-12-31",
        positions=positions,
        base_cur="USD",
        horizon=1,
        signif_level=0.975,
        volatility_id="point_in_time",
        report_depth=0,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-risk-component"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_delta_vector(date, positions, base_cur=None, horizon=None,
                                  signif_level=None, volatility_id=None,
                                  report_depth=None, simplify=False):
    """
    Function to calculate the delta vector of a portfolio

    This function sends a POST request to the 'portfolio-delta-vector' API endpoint
    to calculate the delta vector of a portfolio on a specified date.
    It requires an access token, a date, and the positions in the portfolio.
    It also allows for optional parameters like base currency, horizon,
    volatility ID, and report depth. It returns the response from the API.

    Parameters:
    date (str): A string containing the date for the calculation.
    positions (DataFrame): A DataFrame containing the positions in the portfolio.
    base_cur (str, optional): An optional string containing the base currency.
    horizon (int, optional): An optional numeric containing the horizon.
    signif_level (float, optional): An optional numeric containing the significant level.
    volatility_id (str, optional): An optional string containing the volatility ID.
    report_depth (int, optional): An optional numeric containing the report depth.
    simplify (bool, optional): An optional logical value indicating whether to simplify the
    return values.

    Returns:
    DataFrame: A processed portfolio return value.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })

    delta_vector_1 = envrsk_portfolio_delta_vector(
        date="2022-12-31", 
        positions=positions)

    delta_vector_2 = envrsk_portfolio_delta_vector(
        date="2022-12-31",
        positions=positions,
        base_cur="USD",
        horizon=1,
        volatility_id="point_in_time",
        report_depth=0,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-delta-vector"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "volatility_id": volatility_id,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_economic_capital_regular(date, positions, base_cur=None, horizon=None,
                                              signif_level=None, volatility_id=None,
                                              expected_roe=None, report_depth=None, 
                                              simplify=False):
    """
    Function to calculate the economic capital of a portfolio

    This function sends a POST request to the 'portfolio-economic-capital-regular'
    API endpoint to calculate the economic capital of a portfolio on a specified date.
    It requires an access token, a date, and the positions in the portfolio.
    It also allows for optional parameters like base currency, horizon,
    volatility ID, expected ROE (Return on Equity), and report depth.
    It returns the response from the API.

    Parameters:
    date (str): A string containing the date for the calculation.
    positions (DataFrame): A DataFrame containing the positions in the portfolio.
    base_cur (str, optional): An optional string containing the base currency.
    horizon (int, optional): An optional numeric containing the horizon.
    signif_level (float, optional): An optional numeric containing the significant level.
    volatility_id (str, optional): An optional string containing the volatility ID.
    expected_roe (float, optional): An optional numeric containing the expected Return on
    Equity (ROE).
    report_depth (int, optional): An optional numeric containing the report depth.
    simplify (bool, optional): An optional logical value indicating whether to simplify the
    return values.

    Returns:
    DataFrame: A processed portfolio return value.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })

    economic_capital_1 = envrsk_portfolio_economic_capital_regular(date="2022-12-31", 
                                                                   positions=positions)

    economic_capital_2 = envrsk_portfolio_economic_capital_regular(
        date="2022-12-31",
        positions=positions,
        base_cur="USD",
        horizon=10,
        signif_level=0.99,
        volatility_id="downturn",
        expected_roe=0.10,
        report_depth=0,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-economic-capital-regular"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "expected_roe": expected_roe,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_economic_capital_component(date, positions, base_cur=None, horizon=None,
                                                signif_level=None, volatility_id=None,
                                                expected_roe=None, report_depth=None, 
                                                simplify=False):
    """
    Function to calculate the component economic capital of a portfolio

    This function sends a POST request to the 'portfolio-economic-capital-component'
    API endpoint to calculate the economic capital of a portfolio on a specified date.
    It requires an access token, a date, and the positions in the portfolio.
    It also allows for optional parameters like base currency, horizon,
    volatility ID, expected ROE (Return on Equity), and report depth.
    It returns the response from the API.

    Parameters:
    date (str): A string containing the date for the calculation.
    positions (DataFrame): A DataFrame containing the positions in the portfolio.
    base_cur (str, optional): An optional string containing the base currency.
    horizon (int, optional): An optional numeric containing the horizon.
    signif_level (float, optional): An optional numeric containing the significant level.
    volatility_id (str, optional): An optional string containing the volatility ID.
    expected_roe (float, optional): An optional numeric containing the expected Return on
    Equity (ROE).
    report_depth (int, optional): An optional numeric containing the report depth.
    simplify (bool, optional): An optional logical value indicating whether to simplify the
    return values.

    Returns:
    DataFrame: A processed portfolio return value.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })

    economic_capital_1 = envrsk_portfolio_economic_capital_component(date="2022-12-31", 
                                                                     positions=positions)

    #Print the assumption behind the calculation
    economic_capital_1['Input']

    #Print the result
    economic_capital_1['Output'].merge(
        economic_capital_1['Positions_Mapped'][['symbol', 'uid', 'name']], 
        left_on='UID', 
        right_on='uid',
        how='left')[['UID', 'symbol', 'name', 'Location', 'PortfolioTreeDepthLevel', 'PortfolioType', 'EconomicCapital', 'CostOfRisk']]
                       
    # Explicitly specify the more of the parameters
    economic_capital_2 = envrsk_portfolio_economic_capital_component(
        date="2022-12-31",
        positions=positions,
        base_cur="USD",
        horizon=10,
        signif_level=0.99,
        volatility_id="downturn",
        expected_roe=0.10,
        report_depth=0,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-economic-capital-component"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "expected_roe": expected_roe,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_hyp_rskadj_perf_regular(date, positions, base_cur=None, horizon=None,
                                             signif_level=None, volatility_id=None,
                                             expected_roe=None, report_depth=None, 
                                             simplify=False):
    """
    Function to compute Portfolio Hypothetical Risk Adjusted Performance (Regular)

    This function communicates with a given API endpoint to compute and return the
    hypothetical risk adjusted performance of a given portfolio,
    considering positions provided.

    Parameters:
    date (str): A string in the format 'yyyy-mm-dd', required for the API call. 
    The date of the portfolio.
    positions (DataFrame): A DataFrame representing each row as a position in 
    the portfolio with necessary details.
    base_cur (str, optional): A string representing the base currency for the portfolio.
    horizon (int, optional): The time horizon in days for which the value at risk is calculated.
    signif_level (float, optional): The significance level for the value at risk calculation.
    volatility_id (str, optional): An identifier for a specific volatility model to use in the calculation.
    expected_roe (float, optional): Expected return on equity, as a decimal.
    report_depth (int, optional): The depth to which the report should calculate risk.
    simplify (bool, optional): Logical indicating whether the result should be simplified, if possible.

    Returns:
    Dictionary: If simplify=False, a dictionary with the following components is returned:
    - "Input": A list containing the input parameters used in the API call.
    - "tech_opr": The timestamp of when the API call was made.
    - "Output": A DataFrame with the calculated risk performance.
    - "symbols_mapped": A DataFrame with the symbol mapping.
    - "symbols_unmapped": A DataFrame with the symbols that could not be mapped.
    If simplify=True, only the "Output" DataFrame is returned.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })

    result = envrsk_portfolio_hyp_rskadj_perf_regular(
        date="2023-05-20",
        positions=positions,
        base_cur="USD",
        horizon=1,
        signif_level=0.95,
        expected_roe=0.1,
        report_depth=3,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-hyp-rskadj-perf-regular"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "expected_roe": expected_roe,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)
        
        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_hyp_rskadj_perf_component(date, positions, base_cur=None, horizon=None,
                                               signif_level=None, volatility_id=None,
                                               expected_roe=None, report_depth=None, 
                                               simplify=False):
    """
    Function to compute Portfolio Hypothetical Risk Adjusted Performance (Component)

    This function communicates with a given API endpoint to compute and return the
    hypothetical risk adjusted performance of a given portfolio,
    considering positions provided.

    Parameters:
    date (str): A string in the format 'yyyy-mm-dd', required for the API call. 
    The date of the portfolio.
    positions (DataFrame): A DataFrame representing each row as a position in 
    the portfolio with necessary details.
    base_cur (str, optional): A string representing the base currency for the portfolio.
    horizon (int, optional): The time horizon in days for which the value at risk is calculated.
    signif_level (float, optional): The significance level for the value at risk calculation.
    volatility_id (str, optional): An identifier for a specific volatility model to use in the calculation.
    expected_roe (float, optional): Expected return on equity, as a decimal.
    report_depth (int, optional): The depth to which the report should calculate risk.
    simplify (bool, optional): Logical indicating whether the result should be simplified, if possible.

    Returns:
    Dictionary: If simplify=False, a dictionary with the following components is returned:
    - "Input": A list containing the input parameters used in the API call.
    - "tech_opr": The timestamp of when the API call was made.
    - "Output": A DataFrame with the calculated risk performance.
    - "symbols_mapped": A DataFrame with the symbol mapping.
    - "symbols_unmapped": A DataFrame with the symbols that could not be mapped.
    If simplify=True, only the "Output" DataFrame is returned.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })

    result = envrsk_portfolio_hyp_rskadj_perf_component(
        date="2023-05-20",
        positions=positions,
        base_cur="USD",
        horizon=1,
        signif_level=0.95,
        expected_roe=0.1,
        report_depth=3,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-hyp-rskadj-perf-component"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "expected_roe": expected_roe,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def envrsk_portfolio_hypothetical_performance(date, positions, base_cur=None, report_depth=None, simplify=False):
    """
    Function to calculate the hypothetical performance of a portfolio over a given time period.

    This function sends a request to an external API endpoint and processes the return values.

    Parameters:
    date (str): A string representing the date for the performance calculation.
    positions (DataFrame): A DataFrame representing the portfolio positions.
    base_cur (str, optional): A string representing the base currency for the calculation.
    report_depth (int, optional): The depth of the report.
    simplify (bool, optional): If True, the result is simplified to a vector or matrix if possible.

    Returns:
    Object: Processed portfolio return values based on the response from the API call.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })
    
    port_hyp_perf_1 = envrsk_portfolio_hypothetical_performance(
        date="2023-06-30",
        positions=positions
    )

    port_hyp_perf_2 = envrsk_portfolio_hypothetical_performance(
        date="2023-06-30",
        positions=positions,
        base_cur="USD",
        report_depth=0,
        simplify=True
    )
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "portfolio-hyp-perf"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "report_depth": report_depth
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        positions_dict = pd.DataFrame(positions).to_dict('list')
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions_dict)

        out = process_portfolio_return_values(res_out, simplify)
        return out

def process_portfolio_return_values(res_out, simplify):
    """ Internal function
    Process API Response.

    This function processes the response from the portfolio risk API.
    It concatenates rows of the 'Output', 'Positions_Mapped', and 'Positions_UnMapped' lists
    into data frames using the 'concat' function from the 'pandas' library.
    If the 'simplify' parameter is True, it returns only the 'Output' data frame;
    otherwise, it returns the entire response.

    Parameters:
    res_out (dict): A dictionary containing the API response.
    simplify (bool): A boolean value indicating whether to simplify the return values.

    Returns:
    dict or DataFrame: A list or a data frame depending on the 'simplify' parameter.
                       If the API response status code is not 200, it returns the original response.

    Examples:
    processed_output = process_portfolio_return_values(res_out = api_response, simplify = True)
    """
    if res_out["status_code"] == 200:
        out = res_out["content"]

        if out.get("Output"):
            output = out["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')
            out["Output"] = df_output

        if out.get("Positions_Mapped"):
            pos_mapped = out["Positions_Mapped"]
            df_pos_mapped = pd.DataFrame.from_dict(pos_mapped, orient='columns')
            out["Positions_Mapped"] = df_pos_mapped

        if out.get("Positions_UnMapped"):
            pos_unmapped = out["Positions_UnMapped"]
            df_pos_unmapped = pd.DataFrame.from_dict(pos_unmapped, orient='columns')
            out["Positions_UnMapped"] = df_pos_unmapped

        if simplify:
            return out["Output"]
        else:
            return out
    else:
        return res_out

#******************************************************************************
#### Instrument Functions                                                  ####
#******************************************************************************
def envrsk_instrument_search(partial_name=None, partial_symbol=None, partial_exchange_id=None, position_type=None, valid_at=None):
    """
    Function to search for financial instruments by partial name, symbol, exchange ID, or position type.

    This function calls the 'search-instrument' endpoint of the EnvisionRisk API. The search is done based on the current or specified date.

    Parameters:
    partial_name (str, optional): A partial name of the financial instrument.
    partial_symbol (str, optional): A partial symbol of the financial instrument.
    partial_exchange_id (str, optional): A partial exchange ID of the financial instrument.
    position_type (str, optional): The type of position to search for.
    valid_at (str, optional): Date at which the financial instrument must be valid (YYYY-MM-DD).

    Returns:
    DataFrame: A DataFrame containing the details of the instruments matching the search criteria, 
               or the original API response if the status code is not 200.

    Examples:
    instruments = envrsk_instrument_search(partial_name = "AAPL")
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "search-instrument"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "partial_name": partial_name,
            "partial_symbol": partial_symbol,
            "partial_exchange_id": partial_exchange_id,
            "position_type": position_type,
            "valid_at": valid_at
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body={})

        if res_out["status_code"] == 200:
            out = res_out["content"]["Output"]
            df_output = pd.DataFrame.from_dict(out, orient='columns')         
        else:
            return res_out

        return df_output

def envrsk_instrument_performance(symbols, base_cur=None, from_date=None, to=None, days=1, direction="lead", overlap=True):
    """
    Function to retrieve performance data for a set of financial instruments.

    This function calls the 'instrument-performance' endpoint of the EnvisionRisk API. The performance is calculated over a specified period and frequency.

    Parameters:
    symbols (list): The symbols of the financial instruments for which performance data is required.
    base_cur (str, optional): The base currency in which the performance is calculated.
    from_date (str, optional): The start date for the performance period (YYYY-MM-DD).
    to (str, optional): The end date for the performance period (YYYY-MM-DD).
    days (int, optional): The frequency at which performance data is calculated.
    direction (str, optional): Whether the performance is calculated in a leading ('lead') or lagging ('lag') manner.
    overlap (bool, optional): Whether overlapping returns are allowed in the calculation.

    Returns:
    dict: A dictionary containing the input parameters, the time of operation, 
          the output performance data, and details of mapped and unmapped symbols. 
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    performance = envrsk_instrument_performance(symbols = ["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-performance"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "base_cur": base_cur,
            "from": from_date,
            "to": to,
            "days": days,
            "direction": direction,
            "overlap": overlap
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_performance_raw(symbols, from_date=None, to=None, days=1, direction="lead", overlap=True):
    """
    Function to retrieve performance data for a set of financial instruments.

    This function calls the 'instrument-performance-raw' endpoint of the EnvisionRisk API. 
    The performance is calculated over a specified period and frequency.

    Parameters:
    symbols (list): The symbols of the financial instruments for which performance data is required.
    from_date (str, optional): The start date for the performance period (YYYY-MM-DD).
    to (str, optional): The end date for the performance period (YYYY-MM-DD).
    days (int, optional): The frequency at which performance data is calculated.
    direction (str, optional): Whether the performance is calculated in a leading ('lead') or lagging ('lag') manner.
    overlap (bool, optional): Whether overlapping returns are allowed in the calculation.

    Returns:
    dict: A dictionary containing the input parameters, the time of operation, 
          the output performance data, and details of mapped and unmapped symbols. 
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    performance = envrsk_instrument_performance_raw(symbols = ["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-performance-raw"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "from": from_date,
            "to": to,
            "days": days,
            "direction": direction,
            "overlap": overlap
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_value_at_risk(date, symbols, base_cur=None, horizon=None, signif_level=None, volatility_id=None):
    """
    Function to compute the Value at Risk (VaR) for a set of financial instruments.

    This function calls the 'instrument-value-at-risk' endpoint of the EnvisionRisk API.
    VaR is a statistical measure that quantifies the level of financial risk within
    a firm or investment portfolio over a specific time frame.

    Parameters:
    date (str): The date at which VaR is to be computed (YYYY-MM-DD).
    symbols (list): The symbols of the financial instruments for which VaR is to be computed.
    base_cur (str, optional): The base currency in which VaR is to be computed.
    horizon (float, optional): The time horizon (in days) over which VaR is computed. horizon > 0.01 
    signif_level (float, optional): The significance level for the VaR calculation (between 0 and 1).
    volatility_id (str, optional): The ID of the volatility model to be used. ("point_in_time", "downturn")

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output VaR data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    var = envrsk_instrument_value_at_risk(date = "2023-06-01", symbols = ["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-value-at-risk"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_value_at_risk_raw(date, symbols, horizon=None, signif_level=None, volatility_id=None):
    """
    Function to compute the Value at Risk (VaR) for a set of financial instruments.

    This function calls the 'instrument-value-at-risk-raw' endpoint of the EnvisionRisk API.
    VaR is a statistical measure that quantifies the level of financial risk within
    a firm or investment portfolio over a specific time frame.

    Parameters:
    date (str): The date at which VaR is to be computed (YYYY-MM-DD).
    symbols (list): The symbols of the financial instruments for which VaR is to be computed.
    horizon (float, optional): The time horizon (in days) over which VaR is computed. horizon > 0.01 
    signif_level (float, optional): The significance level for the VaR calculation (between 0 and 1).
    volatility_id (str, optional): The ID of the volatility model to be used. ("point_in_time", "downturn") 

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output VaR data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    var = envrsk_instrument_value_at_risk_raw(date = "2023-06-01", symbols = ["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-value-at-risk-raw"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_expected_shortfall(date, symbols, base_cur=None, horizon=None, signif_level=None, volatility_id=None):
    """
    Function to compute the Expected Shortfall (ES) for a set of financial instruments.

    This function calls the 'instrument-expected-shortfall' endpoint of the EnvisionRisk API.
    ES, also known as Conditional Value at Risk (CVaR), is a risk measure that quantifies the
    expected value of loss given that an event beyond the VaR threshold has occurred.

    Parameters:
    date (str): The date at which ES is to be computed (YYYY-MM-DD).
    symbols (list): The symbols of the financial instruments for which ES is to be computed.
    base_cur (str, optional): The base currency in which ES is to be computed.
    horizon (float, optional): The time horizon (in days) over which ES is computed. horizon > 0.01 
    signif_level (float, optional): The significance level for the ES calculation (between 0 and 1).
    volatility_id (str, optional): The ID of the volatility model to be used. ("point_in_time", "downturn") 

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output ES data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    es = envrsk_instrument_expected_shortfall(date = "2023-06-01", symbols = ["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-expected-shortfall"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_expected_shortfall_raw(date, symbols, horizon=None, signif_level=None, volatility_id=None):
    """
    Function to compute the Expected Shortfall (ES) for a set of financial instruments.

    This function calls the 'instrument-expected-shortfall-raw' endpoint of the EnvisionRisk API.
    ES, also known as Conditional Value at Risk (CVaR), is a risk measure that quantifies the
    expected value of loss given that an event beyond the VaR threshold has occurred.

    Parameters:
    date (str): The date at which ES is to be computed (YYYY-MM-DD).
    symbols (list): The symbols of the financial instruments for which ES is to be computed.
    horizon (float, optional): The time horizon (in days) over which ES is computed. horizon > 0.01 
    signif_level (float, optional): The significance level for the ES calculation (between 0 and 1).
    volatility_id (str, optional): The ID of the volatility model to be used. ("point_in_time", "downturn") 

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output ES data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    es = envrsk_instrument_expected_shortfall_raw(date = "2023-06-01", symbols = ["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-expected-shortfall-raw"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_delta_vector(date, symbols, base_cur=None, horizon=None, volatility_id=None):
    """
    Function to compute the delta vector for a set of financial instruments.

    This function calls the 'instrument-delta-vector' endpoint of the EnvisionRisk API.
    The delta vector provides the partial derivatives of the financial instruments' value
    with respect to an underlying asset price, providing an indication of the sensitivity of
    the instruments' value to changes in the asset price.

    Parameters:
    date (str): The date at which the delta vector is to be computed (YYYY-MM-DD).
    symbols (list): The symbols of the financial instruments for which the delta vector
                    is to be computed.
    base_cur (str, optional): The base currency in which the delta vector is to be computed.
    horizon (float, optional): The time horizon (in days) over which the delta vector is computed. horizon > 0.01
    volatility_id (str, optional): The ID of the volatility model to be used. ("point_in_time", "downturn")

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output delta vector data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    delta_vec = envrsk_instrument_delta_vector(date = "2023-06-01", symbols = ["AAPL", "GOOGL"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-delta-vector"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "volatility_id": volatility_id
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_instrument_delta_vector_raw(date, symbols, horizon=None, volatility_id=None):
    """
    Function to compute the raw delta vector for a set of financial instruments.

    This function calls the 'instrument-delta-vector-raw' endpoint of the EnvisionRisk API.
    The delta vector provides the partial derivatives of the financial instruments' value
    with respect to an underlying asset price, providing an indication of the sensitivity of
    the instruments' value to changes in the asset price.

    Parameters:
    date (str): The date at which the delta vector is to be computed (YYYY-MM-DD).
    symbols (list): The symbols of the financial instruments for which the delta vector
                    is to be computed.
    horizon (float, optional): The time horizon (in days) over which the delta vector is computed. horizon > 0.01
    volatility_id (str, optional): The ID of the volatility model to be used. ("point_in_time", "downturn")

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output delta vector data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    delta_vec_raw = envrsk_instrument_delta_vector_raw(date="2023-06-01", symbols=["AAPL", "GOOGL"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "instrument-delta-vector-raw"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "date": date,
            "horizon": horizon,
            "volatility_id": volatility_id
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

#******************************************************************************
#### Time Series Functions                                                 ####
#******************************************************************************
def envrsk_market_price(symbols, base_cur=None):
    """
    Function to obtain the market prices for a set of financial instruments.

    This function calls the 'market-price' endpoint of the EnvisionRisk API.
    The prices are reported in the specified base currency.

    Parameters:
    symbols (list): The symbols of the financial instruments for which the
                    market prices are to be obtained.
    base_cur (str, optional): The base currency in which the market prices are to
                              be reported.

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output market price data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    market_prices = envrsk_market_price(symbols=["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "market-price"
        api_url = get_api_url(end_point)

        # Query parameters
        params = {
            "base_cur": base_cur
        }
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}    
        
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_market_price_raw(symbols):
    """
    Function to obtain the market prices for a set of financial instruments.

    This function calls the 'market-price-raw' endpoint of the EnvisionRisk API.
    The prices are reported in the specified base currency.

    Parameters:
    symbols (list): The symbols of the financial instruments for which the
                    market prices are to be obtained.

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output market price data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    market_prices = envrsk_market_price_raw(symbols=["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "market-price-raw"
        api_url = get_api_url(end_point)

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params={}, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_market_volatility(symbols):
    """
    Function to obtain the market volatilities for a set of financial instruments.

    This function calls the 'market-volatility' endpoint of the EnvisionRisk API.

    Parameters:
    symbols (list): The symbols of the financial instruments for which the
                    market volatilities are to be obtained.

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output market volatility data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    market_volatilities = envrsk_market_volatility(symbols=["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "market-volatility"
        api_url = get_api_url(end_point)

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params={}, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {
                "Input": out_raw["Input"],
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

def envrsk_market_stress_volatility(symbols):
    """
    Function to obtain the market stress volatilities for a set of financial instruments.

    This function calls the 'market-stress-volatility' endpoint of the EnvisionRisk API.

    Parameters:
    symbols (list): The symbols of the financial instruments for which the
                    market stress volatilities are to be obtained.

    Returns:
    dict: A dictionary containing the input parameters, the time of operation,
          the output market stress volatility data, and details of mapped and unmapped symbols.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    stress_volatilities = envrsk_market_stress_volatility(symbols=["AAPL.US", "DANSKE.CO"])
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "market-stress-volatility"
        api_url = get_api_url(end_point)

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params={}, body=symbols)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            output = out_raw["Output"]
            df_output = pd.DataFrame.from_dict(output, orient='columns')        

            symbs_mapped = out_raw["Symbols_Mapped"]
            df_symbs_mapped = pd.DataFrame.from_dict(symbs_mapped, orient='columns')
            
            symbs_unmapped = out_raw["Symbols_UnMapped"]
            df_symbs_unmapped = pd.DataFrame.from_dict(symbs_unmapped, orient='columns')        

            out = {            
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": df_output,
                "symbols_mapped": df_symbs_mapped,
                "symbols_unmapped": df_symbs_unmapped
            }
        else:
            return res_out

        return out

#******************************************************************************
#### Manifest Functions                                                    ####
#******************************************************************************
def envrsk_get_manifest():
    """
    Function to obtain the manifest, which includes available parameters for portfolio 
    construction and risk computation.

    This function calls the 'get-manifest' endpoint of the EnvisionRisk API.

    Returns:
    dict: If the API call is successful, a dictionary containing the manifest data is
          returned, with portfolio constituents combined into a single list.
          If the API call is unsuccessful, the original API response is returned.

    Examples:
    manifest = envrsk_get_manifest()    
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "get-manifest"
        api_url = get_api_url(end_point)

        res_out = envrsk_get(url=api_url, access_token=get_access_token(), params={}) 

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]
        else:
            return res_out.json()

        return out_raw

def envrsk_update_manifest(manifest):
    """
    **** THIS FUNCTION DOES NOT WORK YET ****
    Function to update the specified manifest.

    This function makes an HTTP POST request to the 'put-manifest' API endpoint
    to update the specified manifest.

    Args:
    manifest (dict): A dictionary, DataFrame or other structure that holds the manifest
                     to be updated. This must match the format expected by the API.

    Returns:
    None: If the API request is successful (i.e., HTTP status code 200),
          this function prints a success message and returns None. If the API request
          is not successful, this function returns the full response from the API.

    Examples:
    # Update a manifest with data    
    my_manifest = envrsk_get_manifest()
    my_manifest["BASE_CUR"] = "USD"
    my_manifest["SIGNIF_LEVEL"] = 0.90
    my_manifest.pop('PORT_CONSTITUENTS')
       
    my_manifest = "{'SIGNIF_LEVEL': 0.90, 'BASE_CUR': 'USD'}"
    envrsk_update_manifest(my_manifest)
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "put-manifest"
        api_url = get_api_url(end_point)
        
        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params={}, body=manifest)

        if res_out["status_code"] == 200:
            print("OK - Manifest updated")
        else:
            return res_out

def envrsk_manifest_restore_to_default():
    """
    Function to restore the default configuration of the manifest.

    This function sends a GET request to the 'restore-manifest' API endpoint
    to restore the default configuration of the manifest. If the status code 
    of the response is 200, it prints a success message. Otherwise, 
    it returns the whole response.

    Returns:
    None: If the API request is successful (i.e., HTTP status code 200),
          this function prints a success message and returns None. If the API request
          is not successful, this function returns the full response from the API.

    Examples:
    envrsk_manifest_restore_to_default()
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "restore-manifest"
        api_url = get_api_url(end_point)

        res_out = envrsk_get(url=api_url, access_token=get_access_token(), params={}) 

        if res_out["status_code"] == 200:
            print("OK - Manifest restored")
        else:
            return res_out

#******************************************************************************
#### Workflow Functions                                                    ####
#******************************************************************************
def envrsk_workflow_backtest(backtestdata, base_cur=None, signif_level=None):
    """
    Function to conduct a backtest for VaR and ES predictions.

    Parameters:
    backtestdata (pd.DataFrame): A dataset used for backtesting.
    base_cur (str, optional): The base currency used for VaR, ES, and the returns.
    signif_level (float, optional): The significance level used for the calculation of VaR & ES.

    Returns:
    dict or requests.Response: If the API call is successful (i.e., HTTP status code 200), 
    the function returns a dictionary containing 'Title', 'Input' 
    (which includes 'backtestdata', 'base_cur', 'signif_level'), 'TechOpr', and 'Output'. 
    If the API call fails, it returns the original output from the API call 
    which includes the status code and error message.

    Examples:
    backtestdata = pd.read_csv('https://www.dropbox.com/scl/fi/dmsiyz8vjxhojmle7bbzw/backtestdata.csv?rlkey=g2olvbo4wlzw0n1qlu0ga2pbe&raw=true')
    df_backtestdata = pd.DataFrame(backtestdata).to_dict('list')
       
    result_backtest = envrsk_workflow_backtest(backtestdata=df_backtestdata, base_cur="DKK", signif_level=0.975)
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "workflow-backtest"
        api_url = get_api_url(end_point)

        params = {
            "base_cur": base_cur,
            "signif_level": signif_level
        }
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=backtestdata)

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            backtestdata_in = out_raw["Input"]["BacktestData"]
            dt_backtestdata_in = pd.DataFrame.from_dict(backtestdata_in, orient='columns')        

            backtestdata_out = out_raw["Output"]
            dt_backtestdata_out = pd.DataFrame.from_dict(backtestdata_out, orient='columns')        
            
            out = {
                "Input": {
                    "backtestdata": dt_backtestdata_in,
                    "base_cur": out_raw["Input"]["BaseCur"],
                    "signif_level": out_raw["Input"]["SignifLevel"]
                },
                "tech_opr": pd.Timestamp.now(),  # Current time
                "Output": dt_backtestdata_out
            }       
        else:
            return res_out

        return out   
 
def envrsk_workflow_risk_snapshot(date, positions, base_cur=None, horizon=None, signif_level=None, 
                                  volatility_id=None, risk_measure=None, report_depth=None, simplify=False):
    """
    Function to run a workflow risk snapshot which calculates risk measures for a portfolio of positions.

    Parameters:
    date (str): The date for which to run the risk snapshot.
    positions (pd.DataFrame): The positions data.
    base_cur (str, optional): The base currency to use for the risk calculations.
    horizon (int, optional): The horizon for the risk calculations.
    signif_level (float, optional): The significance level for the risk calculations.
    volatility_id (str, optional): The volatility id to use for the risk calculations.
    risk_measure (str, optional): The risk_measure signify what risk measure to use in the report. 
                                  Options are 'VaR' or 'ES'.
    report_depth (int, optional): The depth of the report to be generated.
    simplify (bool, optional): If True, the output is simplified.

    Returns:
    dict or requests.Response: A list containing the inputs, technical operations, positions, 
    portfolio delta vector, portfolio risk, mapped positions, and unmapped positions.

    Examples:
    positions = pd.DataFrame({
        "symbol": ["AAPL.US", "DANSKE.CO", "CashUSD", "AGG.US"],
        "position_type": ["single_stock", "single_stock", "cash", "etf"],
        "quantity": [129, 768, 69000, 89]
    })
    df_positions = pd.DataFrame(positions).to_dict('list')
    response_risk_snapshot_1 = envrsk_workflow_risk_snapshot(date="2022-01-01", positions=df_positions)
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        end_point = "workflow-risk-snapshot"
        api_url = get_api_url(end_point)

        params = {
            "date": date,
            "base_cur": base_cur,
            "horizon": horizon,
            "signif_level": signif_level,
            "volatility_id": volatility_id,
            "risk_measure": risk_measure,
            "report_depth": report_depth
        }
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=positions)    

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            out = {
                "Input": out_raw["Input"],
                "tech_opr": out_raw["tech_opr"],
                "positions": pd.DataFrame(out_raw["positions"]),
                "portfolio_delta_vector": pd.DataFrame(out_raw["portfolio_delta_vector"]),
                "portfolio_risk": pd.DataFrame(out_raw["portfolio_risk"]),
                "positions_mapped": pd.DataFrame(out_raw["Positions_Mapped"]),
                "positions_unmapped": pd.DataFrame(out_raw["Positions_UnMapped"])
            }
        else:
            return res_out

        return out

def envrsk_workflow_weight_2_quantities(dt_snapshot_weight, init_port_market_value, base_cur,
                                        is_wide=False, to_date=None):
    """
    Function to calculate quantities based on weights in a portfolio.

    Parameters:
    dt_snapshot_weight (pd.DataFrame): A data table that contains portfolio weights at a certain date.
    init_port_market_value (float): A numeric value that represents the initial market value of the portfolio.
    base_cur (str): A character string that specifies the base currency for the calculation.
    is_wide (bool, optional): A logical value that indicates whether the input data table is in 'wide' format.
    to_date (str, optional): A character string or datetime object representing the ending date for the calculation. 

    Returns:
    dict or requests.Response: A list containing 'Title', 'Input', 'TechOpr', 'Output', and 'UnMappedSymbols'. 

    Examples:
    snapshot_weight = pd.read_csv('https://www.dropbox.com/scl/fi/6wku2orxkrddil5i0r6kl/portfolio_weights_wide.csv?rlkey=tn24ohjin19tki4wmym341s8q&raw=True')
    df_snapshot_weight = pd.DataFrame(snapshot_weight).to_dict('list')
    result_weights_2_quantities = envrsk_workflow_weight_2_quantities(
        dt_snapshot_weight=df_snapshot_weight,
        init_port_market_value=1000000,
        base_cur="DKK",
        is_wide=True)
    """
    if os.getenv("LOGGED_IN") != 'Yes':
        return {"message": "Please login before using the functionality - use 'envrsk_auth_log_in()' or 'envrsk_auth_log_in_interactively()'"}
    else:
        if to_date is None:
            to_date = datetime.datetime.now().strftime('%Y-%m-%d')

        end_point = "workflow-weight-2-quantities"
        api_url = get_api_url(end_point)

        params = {
            "init_port_market_value": init_port_market_value,
            "is_wide": is_wide,
            "base_cur": base_cur,
            "to_date": to_date
        }
        params = {k: v for k, v in params.items() if v is not None}

        res_out = envrsk_post(url=api_url, access_token=get_access_token(), params=params, body=dt_snapshot_weight)    

        if res_out["status_code"] == 200:
            out_raw = res_out["content"]

            out = {
                "Title": out_raw["Title"],
                "Input": {
                    "PortfolioWeights": pd.DataFrame(out_raw["Input"]["PortfolioWeights"]),
                    "base_cur": out_raw["Input"]["BaseCur"],
                    "InitMarketValue": out_raw["Input"]["InitMarketValue"]
                },
                "TechOpr": out_raw["TechOpr"],
                "Output": {
                    "PortfolioEvents": pd.DataFrame(out_raw["Output"]["Events"]),
                    "PortfolioQuantites": pd.DataFrame(out_raw["Output"]["Positions"])
                },
                "UnMappedSymbols": pd.DataFrame(out_raw["Output"]["UnmappedSymbols"])
            }
        else:
            return res_out

        return out
