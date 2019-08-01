#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  TeSLA Admin
#  Copyright (C) 2019 Universitat Oberta de Catalunya
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, time
from OpenSSL import crypto, SSL
import base64, requests
from xml.etree import ElementTree
from tesla_admin.blueprints.system.cawrapper.Exceptions import CertificateFileMissing
from tesla_admin import logger, app

def get_x509_cerificate(service_name, certificate_type, key_or_cert):
    service_split = service_name.split("-")
    service_name_only = service_name.replace("-"+service_split[-1], "")

    public_services = ["tep", "tip", "tup", "portal", "registry", "rt", "lti", "moodle", "kibana", "broker", "admin", "vle", "api", "flower"]
    cn = str(service_name_only)+"."+str(app.config['DOMAIN'])

    if key_or_cert == 'CA':
        return __get_tesla_ca__()

    if service_name_only in public_services and certificate_type == 'SERVER':
        # get lets encrypt certificate
        return __get_letsencrypt_certificate__(cn, key_or_cert)


    if service_name_only not in public_services or certificate_type == 'CLIENT':
        cn = str(service_name)

    if certificate_type == 'CLIENT':
        cn = service_name.replace("-service", "")
        cn = cn.replace("-worker", "")

    return __get_tesla_certificate__(cn, certificate_type, key_or_cert)


def __get_tesla_certificate__(cn, certificate_type, key_or_cert):
    # check if certificate is in data/certs/modules/{cn} folder

    path = "data"+os.path.sep+"certs"+os.path.sep+"modules"+os.path.sep+cn

    if not os.path.isdir(path):
        os.makedirs(path)

    file = path+os.path.sep+"cert.pem"

    if not os.path.isfile(file):
        # create key and cert tesla pair
        __create_key_and_cert_tesla__(cn, certificate_type)

    if key_or_cert == "KEY":
        file = path+os.path.sep+"key.pem"

    try:
        with open(file, 'r') as infile:
            file_content = ""

            for line in infile:
                file_content = file_content+str(line)

            return file_content
    except:
        raise ValueError("File not found: "+str(file))

    return None


def __create_key_and_cert_tesla__(cn, certificate_type):
    CERT_TYPE_SERVER = "X509_SERVER"
    CERT_TYPE_CLIENT = "X509_CLIENT"
    issuer = "university-intermediate-ca"

    cert_type = CERT_TYPE_CLIENT
    if certificate_type == "SERVER":
        cert_type = CERT_TYPE_SERVER

    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509Req()

    cert.add_extensions([])
    cert.get_subject().C = str(app.config['COUNTRY'])
    cert.get_subject().ST = "Europe"
    cert.get_subject().L = "TeSLA"
    cert.get_subject().O = str(app.config['INSTITUTION'])
    cert.get_subject().OU = cn
    cert.get_subject().CN = cn

    if certificate_type == "CLIENT":
        cert.get_subject().CN = cn+"."+str(app.config['INSTITUTION'])

    cert.set_version(2)

    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    path = "data"+os.path.sep+"certs"+os.path.sep+"modules"+os.path.sep+cn+os.path.sep

    open(path+"cert.csr", "wt").write(
        str(crypto.dump_certificate_request(crypto.FILETYPE_PEM, cert).decode("utf-8")))

    open(path+"key.pem", "wt").write(
        str(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8")))

    x509 = base64.b64encode(crypto.dump_certificate_request(crypto.FILETYPE_PEM, cert))

    xsd = __getRequestXSD__(cn, issuer, x509, cert_type)

    if certificate_type == 'CLIENT':
        xsd = __getRequestXSD__(cn+"."+str(os.getenv('INSTITUTION')), issuer, x509, cert_type)

    headers = {"Content-type": "text/xml"}

    base_path = "data"+os.path.sep+"certs"+os.path.sep+"deploy-manager"+os.path.sep
    dm_cert = base_path+"cert.pem"
    dm_key = base_path+"key.pem"
    ca = base_path+"ca.pem"

    url = "https://ca."+os.getenv('DOMAIN')+"/"+str('certificateRequest')

    #url = "https://ca.test.tesla-project.eu:5000/"+str('certificateRequest')

    response = requests.post(url, data=xsd, cert=(dm_cert, dm_key), verify=ca, headers=headers)

    if response.status_code == 200:
        root = ElementTree.fromstring(response.content)

        for certificates in root.findall('certificates'):
            for certificate in certificates:
                for x509Certificate in certificate:
                    if x509Certificate.tag == 'x509Certificate':
                        for pemData in x509Certificate:
                            if pemData.tag == 'pemData':
                                cert = base64.b64decode(pemData.text).decode("utf-8")
                                open(path+"cert.pem", "wt").write(cert)
    else:
        raise ValueError("ERROR response in CA (status code "+str(response.status_code)+"): "+str(response.content))

    return True


def __get_letsencrypt_certificate__(cn, key_or_cert, try_letsencrypt=True):
    filename = 'cert.pem'

    if key_or_cert == 'KEY':
        filename = 'key.pem'

    file = "data"+os.path.sep+"certs"+os.path.sep+"modules"+os.path.sep+cn+os.path.sep+filename

    try:
        with open(file, 'r') as infile:
            file_content = ""

            for line in infile:
                file_content = file_content+str(line)

            return file_content
    except:
        logger.error("File not found: "+file)
        pass

    raise CertificateFileMissing("File not found: "+file)


def __get_tesla_ca__():

    file = "data"+os.path.sep+"certs"+os.path.sep+"deploy-manager"+os.path.sep+"ca.pem"

    try:
        with open(file, 'r') as infile:
            file_content = ""

            for line in infile:
                file_content = file_content+str(line)

            return file_content
    except:
        logger.error("File not found: "+file)
        pass

    return None


'''
cert = None
CERT_TYPE_SERVER = "X509_SERVER"
CERT_TYPE_CLIENT = "X509_CLIENT"
'''
def __getRequestXSD__(cn, issuer, x509, certificateType):
    xsd = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\
            <csb:certificateStore xmlns:csb="http://www.stonepine.fr/certificateStoreBinding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.stonepine.fr/certificateStoreBinding/ ../xsd/certificateStore.xsd">\
            <certificateRequests>\
               <certificateRequest>\
                    <subjectCommonName>'+str(cn)+'</subjectCommonName>\
                    <issuerCommonName>'+str(issuer)+'</issuerCommonName>\
                    <x509CertificateType>'+str(certificateType)+'</x509CertificateType>\
                    <x509CertificateRequest>\
                        <pemData>'+str(x509.decode("utf-8"))+'</pemData>\
                    </x509CertificateRequest>\
                </certificateRequest>\
            </certificateRequests>\
            </csb:certificateStore>'

    return xsd


def revoke_x509_cerificate(cn, certificate_type):
    issuer = "university-intermediate-ca"
    CERT_TYPE_SERVER = "X509_SERVER"
    CERT_TYPE_CLIENT = "X509_CLIENT"

    if certificate_type == 'CLIENT':
        cn = cn.replace("-service", "")
        cn = cn.replace("-worker", "")
        cn = str(cn) + os.getenv("INSTITUTION")
