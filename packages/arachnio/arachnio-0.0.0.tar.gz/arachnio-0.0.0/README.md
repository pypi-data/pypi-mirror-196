# arachnio4j [![tests](https://github.com/arachnio/arachnio4py/actions/workflows/tests.yml/badge.svg)](https://github.com/arachnio/arachnio4py/actions/workflows/tests.yml)

[Arachnio](https://www.arachn.io/) client library for Python 3.10+

## Getting Started

### Step 1. Subscribe 👍

First, you'll need to subscribe to [an Arachnio product](https://developer.arachn.io/catalog). The [Free Forever Plan](https://developer.arachn.io/catalog/prd_2jlyolt6e0gkaur4) is just fine for this introduction. Before we head to the next step, you'll need your Base Product URL and one of your Bloblr API Keys.

![The Subscription Authentication Screen](https://arachnio-web-assets.s3.us-east-2.amazonaws.com/images/introduction-base-url-and-blobr-api-keys.png)

Above is a screenshot of the Subscription Authentication screen, which contains these facts. The Base Product URL is circled in red, and the Blobr API keys in green. Both are redacted for privacy. 🤫

### Step 2. Pick a Webpage 🔗

In this introduction, we will extract structured data from a webpage, so the next step is to pick a webpage to extract. In the spirit of web crawling, we have picked [an article about spiders](https://www.nytimes.com/2022/08/25/science/spiders-misinformation-rumors.html) for this example. 🕷

![Hey there, fella!](https://arachnio-web-assets.s3.us-east-2.amazonaws.com/images/introduction-spider.jpeg)

### Step 3. Call Link Extract Endpoint 📢

Now that we have our base URL, API key, and parameters, we can call the link extract endpoint!

    from arachnio import ArachnioClient
    
    # ARACHNIO_BASE_URL and BLOBR_API_KEY are from Step 1
    client = ArachnioClient(ARACHNIO_BASE_URL, BLOBR_API_KEY)
    
    # The link is from Step 2
    response = client.extractLink(
        "https://www.nytimes.com/2022/08/25/science/spiders-misinformation-rumors.html")
        
    entity = response["entity"]

    if entity["entityType"]=="webpage" and entity["webpageType"]=="article":
        print(entity["title"]);
        # Spiders Are Caught in a Global Web of Misinformation
