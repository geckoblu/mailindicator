import os
import unittest

import urllib, ssl


class TestCertificate(unittest.TestCase):
    
    context = ssl.create_default_context()
    context.load_verify_locations(cafile = "/home/alessio/old_home/Documents/Wuerth/Wuerth_CA_Root_Certificate.pem")
    print(context.get_ca_certs())
    urllib.request.urlopen("https://bucket.s3.amazonaws.com/", context=context)
    
if __name__ == "__main__":
    unittest.main()