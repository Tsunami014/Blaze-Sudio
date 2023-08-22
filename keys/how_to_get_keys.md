# How to get API Keys

## How to get Bard's API key

1. Visit [Bard's website](https://bard.google.com/) *on Google Chrome* (will not work in any other browser).
2. F12 for console
3. Session: Application → Cookies → Copy the value of  `__Secure-1PSID` cookie.

> Note that while I referred to `__Secure-1PSID` value as an API key for convenience, it is not an officially provided API key. 
> Cookie value subject to frequent changes. Verify the value again if an error occurs. Most errors occur when an invalid cookie value is entered.
> Also Note that this program uses a separate library to handle this, so as it updates, or if Bing's webpage updates, this may not. (But I hope I can update this in time anyways). Please check [this](https://github.com/dsdanielpark/Bard-API#authentication) website if you need more help/updated support, or you can message me on wherever.

## How to get Bing AI (Sydney)'s API Key

To use Sydney.py you first need to extract the `_U` cookie from [Bing](https://bing.com). The `_U` cookie is used to authenticate your requests to the Bing Chat API.

To get the `_U` cookie, follow these steps:
- Log in to [Bing](https://bing.com) using your Microsoft account *on Microsoft Edge* (will not work in any other browser).
- Open the developer tools in your browser (usually by pressing `F12` or right-clicking and selecting `Inspect element`).
- Select the `Storage` tab and click on the `Cookies` option to view all cookies associated with the website.
- Look for the `_U` cookie and click on it to expand its details.
- Copy the value of the `_U` cookie (it should look like a long string of letters and numbers).

> Please Note that (like the previous one) this program uses a separate library to handle this, so as it updates, or if Bing's webpage updates, this may not. (But I hope I can update this in time anyways). Please check [this](https://github.com/vsakkas/sydney.py/tree/v0.12.0#prerequisites) website if you need more help/updated support, or you can message me on wherever.
