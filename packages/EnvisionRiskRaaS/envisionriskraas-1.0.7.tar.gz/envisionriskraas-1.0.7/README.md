<h1>EnvisionRiskRaaS</h1>
<hr>
Delve into the world of EnvisionRisk’s Python package, your portal to our sophisticated Market Risk-as-a-Service (RaaS). This comprehensive tool allows you to tap into our cutting-edge risk management services, retrieve relevant data, perform complex calculations, and generate actionable insights, all without leaving your Python programming environment. Embrace this smarter, efficient approach to handling market risk.

Are you navigating the volatile waters of financial uncertainties, seeking to make strategic decisions? Allow EnvisionRisk’s Cloud Service to be your compass, providing a precise mechanism for quantifying market risks. Replace guesswork with certainty; our platform furnishes you with standardized metrics designed to enhance cost-efficiency and fortify your financial bulwark.

Our REST API, a seamless blend of security and user-friendliness, stands as your reliable tool for everyday risk quantification. Transform data into actionable steps and unravel the potential concealed within the labyrinth of financial complexities.

With an expansive coverage spanning more than 13,000 exchange-traded and over-the-counter instruments—and continuously growing—EnvisionRisk is primed to adapt to your ever-evolving needs.

Join the EnvisionRisk community today. Convert your market insights into solid foresights, and consistently maintain a competitive edge in the ever-fluctuating financial market. Stay not just in the game, but ahead of it.

<h2>Authentication</h2>
<hr>
EnvisionRisk employs robust authentication and authorization processes to safeguard systems and information. EnvisionRisk’s Market Risk-as-a-Service API operates on a token-based authentication system. To use the service you need to be a registered user. If you don’t already have credentials, you can sign up for a free trial account here:
<a href='https://envisionrisk.shinyapps.io/user_management' target='_blank'><img height='100' style='border:0px;height:100px;' src='https://camo.githubusercontent.com/e757b083ceb7645a42a28ce48d538a7c52808781191546a5cfe1bd6c37c7c677/68747470733a2f2f7777772e64726f70626f782e636f6d2f732f6330616f69363878686d70313132332f7369676e2d75702d627574746f6e2d706e672d33332e706e673f7261773d74727565' border='0' alt='Sign up' /></a>

<h2>Installation</h2>
<hr>
You can install the development version of EnvisionRiskRaaS like so:

```
pip install EnvisionRiskRaaS
```

<h2>Example</h2>
<hr>
Although the following example may appear simple, it’s designed to illustrate how our service functions by requesting the simulated profit/loss (P/L) distribution for a single instrument — Apple (AAPL.US) as of 2023-06-28. Remember, this is just a starting point; our service also allows you to request simulated P/L distribution for your custom portfolios. Through this, you gain invaluable insights into potential future outcomes, enabling you to make informed investment decisions.

The Profit and Loss (P/L) distribution is a crucial component in the world of market risk management as it provides a quantitative way of understanding potential financial outcomes. Here’s why it plays an essential role:

- <b>Risk Assessment:</b> The P/L distribution represents the range of possible gains and losses that a portfolio might experience. It allows risk managers to visualize and quantify potential risks. For example, the tails of the distribution give insight into extreme events and potential for significant losses, enabling a comprehensive risk assessment.

- <b>Risk Measures Calculation:</b> Key risk measures, like Value at Risk (VaR) and Expected Shortfall (ES), are derived from the P/L distribution. VaR estimates the potential loss a portfolio could face over a given period with a certain level of confidence, while ES provides the expected loss given that a loss exceeds the VaR threshold. These metrics help risk managers understand the risk landscape better and make informed decisions.

- <b>Portfolio Optimization:</b> By understanding the P/L distribution, managers can optimize the portfolio for desired outcomes. It allows them to adjust the portfolio composition to control the risk, striking a balance between risk and return.

- <b>Regulatory Compliance:</b> Regulators often require financial institutions to maintain capital reserves based on potential losses, which are derived from P/L distributions. Hence, understanding the P/L distribution is crucial to meet these regulatory requirements.

- <b>Stress Testing:</b> Stress testing involves applying extreme but plausible hypothetical scenarios to the P/L distribution to assess the portfolio’s resilience. This helps managers prepare for unexpected market events and ensure that the portfolio can withstand adverse conditions.

Therefore, P/L distribution serves as a key pillar of market risk management, providing insights into potential risks, informing decision-making, enabling portfolio optimization, and ensuring regulatory compliance.

```
#### Get the delta vector (simulated price change) ####
# The term '_raw' within the function name is indicative of a key feature: 
# the simulated price changes are denominated in the same currency as 
# the stock. This implies that the analysis maintains the original currency 
# perspective of the stock, allowing for more accurate and relevant 
# insights. It enhances ease of comprehension and direct applicability, 
# bringing us closer to the context of the actual trading environment.
api_response = RAAS.envrsk_instrument_delta_vector_raw(use_date,use_symbol)

# Leverage our sophisticated API to conduct an Expected-Shortfall computation, 
# specified at a 97.5% confidence level across a single-day span, utilizing a 
# point-in-time volatility scenario.
api_response_es = RAAS.envrsk_instrument_expected_shortfall_raw(use_date, use_symbol, signif_level = 0.975, volatility_id = "point_in_time")
expected_shortfall_estimate = api_response_es["Output"]["expected_shortfall"][0]

#manipulate the data for the density function
data = api_response["Output"]["PnL"]
density = stats.gaussian_kde(data)

#build a dataset spanning from min of the PnL dataset to the max.
xs = np.linspace(min(data), max(data), 200)
#build weights for the histogram
weights = np.ones_like(data) / len(data)

#indicate the subtitle and the caption text.
subtitle = "Profit/Loss distribution (one day) for " + use_symbol + " as seen from the " + str(use_date)
caption= "In the world of financial markets, price uncertainty is a key element that contributes to market risk - the risk of losses in positions arising \n
from movements in market prices. Risk management aims to quantify this risk and devise strategies to mitigate potential losses."

# Plot the P/L distribution
#title
plt.suptitle("Price Uncertainty", x=0.2875, y=1, fontsize=18)
#subtitle
plt.title(subtitle, fontsize=10, loc='left')

#histogram, density and vertical line.
plt.hist(data, weights=weights, bins=37, color="#27647B", edgecolor="#27647B",alpha = 0.75)
plt.plot( xs, density(xs), color="#CA3542", alpha=0.5)
plt.axvline(x = expected_shortfall_estimate, color = "#57575F", label = 'axvline - full height')

#vertical line text, labels, remove tickers and insert caption
plt.text(expected_shortfall_estimate, max(density(xs))/2, 'Expected-Shortfall (97.5%, 1 day)', ha='center', va='center',rotation='vertical', backgroundcolor='white')
plt.xlabel("Profit/Loss (in $)")
plt.ylabel("Density")
plt.yticks([])
plt.text(0.5, -0.04, caption, ha='center', size=7)
#plot
plt.show()
```

<img height='600' style='border:0px;height:600px;' src='https://raw.githubusercontent.com/EnvisionRisk/EnvisionRiskRaaS/master/man/figures/README-plot-1.png' border='0' />

<h2>API documentation</h2>
<hr>
You can locate our extensive API documentation <a href="https://envisionrisk.stoplight.io/docs/api-aleadomus-documentation/9ed9f79a31a4a-market-risk-as-a-service-api">here</a>. This comprehensive guide is designed to walk you through our APIs’ functionalities, providing clear instructions on how to integrate and use them effectively.

For each API, you’ll find detailed descriptions, parameter information, example requests, and response formats to help you understand the API’s purpose and functionality. Whether you’re interested in user authentication, data retrieval, or performing specific actions, our documentation has you covered.

In addition, you’ll find a section dedicated to ‘Common Use Cases’ where we illustrate how our APIs can be combined and utilized in various scenarios. This can be an invaluable resource for those seeking to maximize the potential of our services.

Please note that our API documentation is constantly updated with new features and improvements to ensure you have the latest information at your fingertips.

Explore our API documentation today to get started with your integrations and to make the most out of our services!






