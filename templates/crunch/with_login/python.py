from collections import OrderedDict
from os import name
import random
import random as rd   
import json
import time
import js2py
from requests_html import HTML


\


qpayRadarID = 'cUXvdB6hHu';
tempfile = js2py.run_file("{js/payment.js}");


session_start();
testMode = True;
sessionID = uniqid()
orgID =  '1snn5n9w' if testMode else 'k8vif92e';
mechantID = 'visanetgt_qpay';


base_api ="https://sandbox.qpaypro.com/payment/api_v1%22"
testMode = True
sessionID = uniqid()
orgID = $testMode ? '1snn5n9w' : 'k8vif92e';
mechantID = 'visanetgt_qpay'

$fingerId = $_GET["fingerId"];
}else{
$fingerId = '';
}

qpayRadarID = 'cUXvdB6hHu';
array = OrderedDict([("x_login","visanetgt_qpay"),
("x_private_key","88888888888"),
("x_api_secret","99999999999"),("x_product_id",6),
("x_audit_number",rd(1.999999)),
("x_fp_sequence",1988679099),("x_fp_timestamp",int(time.time())),
("x_invoice_num",random.randint(1.999999)),
("x_currency_code","GTQ"),
("x_amount",1.0),
("x_line_item","T-shirt Live Dreams<|>w01<|><|>1<|>1000.00<|>N"),
("x_freight",0.0),("x_email","test@email.com"),
("cc_number","4111111111111111"),
("cc_exp","01/30"),
("cc_cvv2","4567"),
("cc_name","johndoe"),
("cc_type","visa"),
("x_first_name","john"),
("x_last_name","doe"),
("x_company","Company"),
("x_address","711-2880 Null"),
("x_city","Guatemala"),
("x_state","Guatemala"),
("x_country","Guatemala"),
("x_zip","01056"),
("x_relay_response","none"),
("x_relay_url","none"),
("x_type","AUTH_ONLY"),
("x_method","CC"),
("http_origin","http://local.test.com"),
("visaencuotas",0),
("device_fingerprint_id",sessionID),
('payment_response_url',OrderedDict([('success_url','https://sandbox.qpaypro.com/integraciones/api-test/api-test-sandbox.php'),
('error_url','https://sandbox.qpaypro.com/integraciones/api-test/api-test-sandbox.php')])),("finger",'')]);

if (isset(_GET["fingerId"])) :
    ch = curl_init();
    curl_setopt(ch, CURLOPT_URL, base_api);
    curl_setopt(ch, CURLOPT_POST, 1);
    curl_setopt(ch, CURLOPT_POSTFIELDS, array);
    curl_setopt(ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt(ch, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt(ch, CURLOPT_SSL_VERIFYPEER, 0);
    resp = curl_exec(ch);
    info = curl_getinfo(ch);
    resp = str(resp, "{", False);
    json = OrderedDict(json.loads(resp));
    print(json);

