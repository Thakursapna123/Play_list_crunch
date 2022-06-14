import hashlib
import hmac
import codecs
import datetime
import requests
import json

def get_headers(merchant_code,secret_key):
        now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        string = str(len(merchant_code)) + merchant_code + str(len(now)) + now
        string = codecs.encode(string)
        secret_key = codecs.encode(secret_key)
        string_hash = hmac.new(secret_key, string, hashlib.md5).hexdigest()
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Avangate-Authentication': 'code="' + merchant_code + '" date="' + now + '" hash="' + string_hash + '"'
        }


def cal_api(ENDPOINT, PARAMS, METHOD,HEADER_DATA):
    base_url = 'https://api.2checkout.com/rest/6.0/'
    main_url = base_url + ENDPOINT
    try:
        response = requests.request(METHOD.upper(), main_url, data=json.dumps(PARAMS), headers=HEADER_DATA)
        return response.text
    except Exception as e:
        raise TwocheckoutError('REQUEST_FAILED', e.args)


def get_params():
    return{
  "Country": "br",
  "Currency": "USD",
  "OrderNo":'5264',
  "CustomerIP": "91.220.121.21",
  "CustomerReference": "GFDFE",
  "ExternalCustomerReference": "IOUER",
  "ExternalReference": "REST_API_AVANGTE",
  "Language": "en",
  "Source": "testAPI.com",
 "Affiliate": {
    "AffiliateCode": "3501E8CADA",
    # "Status": "Active",
    # "Affiliate Name": "Softy Bofty",
    # "Website": "https://softy.fake",
    # "CommissionList": {
    #   "Object": {
    #     "ListName": "CommissionList1",
    #     "CommissionRate": "25%"
    #   }
    # },
    # "RequestDate": "2018-10-05",
    # "Categories": [
    #   [
    #     "PC security",
    #     "Mobile security"
    #   ]
    # ],
    # "TCStatus": "Accepted",
    # "AffiliateContact": {
    #   "Object": {
    #     "FirstName": "John",
    #     "LastName": "Doe",
    #     "Phone": "40723483987",
    #     "Email": "dynamicproduct@products.com",
    #     "Country": "Spain"
    #   }
    # }
  },
  "BillingDetails": {
    "Address1": "Test Address",
    "City": "LA",
    "CountryCode": "BR",
    "Email": "customer@2Checkout.com",
    "FirstName": "Customer",
    "FiscalCode": "056.027.963-98",
    "LastName": "2Checkout",
    "Phone": "556133127400",
    "State": "DF",
    "Zip": "70403-900"
  },
  "Items": [
    {
      "Code": "ail1",
      "Quantity": "1"
    }
  ],
  "PaymentDetails": {
    "Currency": "USD",
    "CustomerIP": "91.220.121.21",
    "PaymentMethod": {
      "CCID": "123",
      "CardNumber": "378282246310005",
      "CardNumberTime": "12",
      "CardType": "AMEX",
      "ExpirationMonth": "12",
      "ExpirationYear": "2022",
      "HolderName": "John Doe",
      "HolderNameTime": "12",
      "RecurringEnabled": True,
      "Vendor3DSReturnURL": "www.test.com",
      "Vendor3DSCancelURL": "www.test.com"
    },
    "Type": "TEST"
  }
}

def set_resource(resource):
    resource_url = resource + '/'
    return resource_url